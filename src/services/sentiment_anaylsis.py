
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models

from dotenv import dotenv_values
import json
from google.oauth2 import service_account
import os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
with open(GOOGLE_API_KEY) as source:
    info = json.load(source)

vertex_credentials = service_account.Credentials.from_service_account_info(info)
vertexai.init(project="lithe-sandbox-444313-n8", location="asia-southeast1")

#Sentiment Class
class SentimentAnalysis:
    def __init__(self, transcript):
        self.transcript = transcript

    def run_sentiment(self):
        generation_config = {
        "max_output_tokens": 2048,
        "temperature": .1,
        "top_p": 1,
    }
        safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }  
        model = GenerativeModel(
        "projects/738905644646/locations/asia-southeast1/endpoints/6471483548531425280",
        system_instruction=["""You are a model able to classify a text"""]
    )
        chat = model.start_chat()
        response = chat.send_message(
        [self.transcript],
        generation_config=generation_config,
        safety_settings=safety_settings
    )
        sentiment = response.candidates[0].content.parts[0].text
        return sentiment

