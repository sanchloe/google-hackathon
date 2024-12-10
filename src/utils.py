import json
import datetime
import uuid
import streamlit as st

from dotenv import load_dotenv

load_dotenv()

def read_transcript(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        transcript = file.read()
    return transcript

def load_template(template_name):
    with open(f'{template_name}.json') as f:
        return json.load(f)

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def save_audio_file(audio_bytes, file_extension):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"audio_{timestamp}.{file_extension}"

    with open(file_name, "wb") as f:
        f.write(audio_bytes)

    return file_name

def setup_session():
    client_name = "John Doe"
    client_id = str(uuid.uuid4())
    therapist_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())
    return session_id, therapist_id, client_id, client_name

def render_sections(section_lst, description_lst, content_lst):
    l = ['']
    for idx, (key, description) in enumerate(zip(section_lst, description_lst)):
        content = content_lst[idx]
        l.append(
            """
                <h4>{}</h4>
                <p>{}</p>
                <p>Content: {}</p>
            """.format(key, description, content)
        )
    return """
        <div style="border: 1px solid #BEC6A0; padding: 10px; border-radius: 5px; margin-bottom: 10px; background-color: white;box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2)">
            {}
        </div>
    """.format('<br>'.join(l))

def update_recommendations(placeholder, category_data, label):
    if len(category_data) > 0:
        recommended_text = " ".join([f'<span class="recommendedtext">{item}</span>' for item in category_data])
        placeholder.markdown(f'<p>{label}: {recommended_text}</p>', unsafe_allow_html=True)
    else:
        placeholder.markdown(f'<p>{label}: None</p>', unsafe_allow_html=True)

def initialize_session_state(keys):
    for key in keys:
        if key not in st.session_state:
            st.session_state[key] = False

def get_selected_keys_string(section_keys):
    # selected_values = {key: st.session_state[key] for key in keys if st.session_state[key]}
    selected_values = {key: st.session_state[key] for key in section_keys if st.session_state[key]}
    selected_keys_string = ", ".join([key for key, value in selected_values.items() if value])
    return selected_keys_string