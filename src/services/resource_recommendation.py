from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_vertexai import ChatVertexAI, HarmBlockThreshold, HarmCategory
from langchain_google_vertexai import VertexAIEmbeddings
from .retriever import Retriever
from ..deployment.vector_search import VectorSearch
import os

load_dotenv()

class ResourceRecommender:
    """A class for recommending resources based on therapy session transcripts."""

    def __init__(self, transcript):
        self.transcript = transcript
        self.vector_search = None

    def get_system_prompt(self):
        """Return the system prompt for the language model."""
        return """You are a therapist assistant tasked with finding the top one most important or critical issues discussed in a therapy session, and using this information to formulate a question in first person perspective that will help with appropriate resource and worksheet retrieval. You will be given a transcript of the session. Only return the question as a string. Do not write any introduction or summary. Here is a sample output:
        
        What can I do to sleep better at night?
        """

    def create_user_prompt(self):
        """Return the user prompt for the language model."""
        return "Here is the transcription of the therapy session: {transcript}\nRespond only with the question. Do not write an introduction or summary."

    def get_question(self):
        """Generate the main question from the transcript."""
        model = ChatVertexAI(
            model_name="gemini-1.5-pro",
            convert_system_message_to_human=True,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            },
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", self.get_system_prompt()),
            ("human", self.create_user_prompt())
        ])

        chain = prompt | model
        input_dict = {
            "transcript": self.transcript,
        }
        response = chain.invoke(input_dict)

        print("Generated Question:", response.content)
        return response.content.strip()

    def initialize_vector_search(self):
        """Initialize the vector search with required configurations."""
        INDEX_ID = os.getenv("INDEX_ID")
        ENDPOINT_ID = os.getenv("ENDPOINT_ID")
        EMBEDDING_MODEL = VertexAIEmbeddings(model_name="text-embedding-005")

        self.vector_search = VectorSearch(
            index_id=INDEX_ID,
            endpoint_id=ENDPOINT_ID,
            embedding_model=EMBEDDING_MODEL,
        )

    def get_recommendations(self):
        """Retrieve resource recommendations based on the generated question."""
        question = self.get_question()

        if self.vector_search is None:
            self.initialize_vector_search()

        retriever = Retriever(self.vector_search.vector_store)
        documents = retriever.retrieve(query=question, top_k=3)
        resource_links = set()
        for document in documents:
            resource_link = document.metadata.get("link")
            if resource_link:
                resource_links.add(resource_link)

        return resource_links
