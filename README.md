# Case Crafter
## Project Description
Case Crafter is an AI tool designed to automate the creation of therapy case notes, saving therapists time and ensuring consistency. After sessions, therapists upload audio recordings, which are transcribed using speech-to-text technology, capturing all key details without manual effort. The platform also includes sentiment analysis to assess emotional tones, offering insights into client progress.

## Installation
1. Clone the repository: `git clone https://github.com/sanchloe/google-hackathon.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in a `.env` file.

## Features
1. Speech to text and speaker diarization
2. Accurate case notes and progress notes generation using Gemini-1.5-flash model
3. Dashboard for mental health insights and metrics
4. Data-driven resource recommendation using Retrieval Augmented Generation (RAG)
5. Sentiment analysis using fine tuned Gemini-1.0-pro model
6. Integration with a database for efficient task management and feedback loop

## Usage
To start the application locally, run:
```bash
uvicorn streamlit run main.py
```
Access the API at: http://localhost:8000/.

## License
This project is licensed under the Apache-2.0 License. See the `LICENSE` file for details.