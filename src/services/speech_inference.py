from google.cloud import speech
from google.protobuf import wrappers_pb2 
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import upload_to_gcs
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
client = speech.SpeechClient.from_service_account_file(GOOGLE_API_KEY)

class SpeechToText:
    def __init__(self, file_path):
        self.file_path = file_path

    def transcribe_speech(self):
        audio = speech.RecognitionAudio(uri=self.file_path)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code="en-US",
            model="latest_long",
            audio_channel_count=1,
            enable_automatic_punctuation=True,
            enable_word_confidence=True,
            enable_word_time_offsets=True,
            enable_spoken_punctuation=wrappers_pb2.BoolValue(value=True),
            diarization_config=speech.SpeakerDiarizationConfig(
                enable_speaker_diarization=True,
                min_speaker_count=2,
                max_speaker_count=6,
            ),
        )

        # Detects speech in the audio file
        operation = client.long_running_recognize(config=config, audio=audio)

        print("Waiting for operation to complete...")
        response = operation.result(timeout=90)

        # Process the diarized result
        speaker_texts = []
        current_speaker = None
        speaker_buffer = []

        for result in response.results:
            for word_info in result.alternatives[0].words:
                speaker = word_info.speaker_tag
                word = word_info.word

                # Skip Speaker 0
                if speaker == 0:
                    continue

                if current_speaker is None or current_speaker != speaker:
                    if speaker_buffer:
                        speaker_texts.append(
                            f"Speaker {current_speaker}: {' '.join(speaker_buffer)}"
                        )
                    current_speaker = speaker
                    speaker_buffer = [word]
                else:
                    speaker_buffer.append(word)

        if speaker_buffer:
            speaker_texts.append(
                f"Speaker {current_speaker}: {' '.join(speaker_buffer)}"
            )
        current_date = datetime.now().strftime("%Y-%m-%d")

        local_file_path = f"transcript_{current_date}.txt"
        with open(local_file_path, "w") as file:
            file.write("\n".join(speaker_texts))

        print(f"Transcription saved to {local_file_path}.")
        file_path = upload_to_gcs("therapy_audio", local_file_path, f"transcripts/{local_file_path}")

        return file_path

