import json
import os

from dotenv import load_dotenv
from google.cloud import aiplatform, storage
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_vertexai import (VectorSearchVectorStore,
                                       VertexAIEmbeddings)
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME")
PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")
INDEX_ID = os.getenv("INDEX_ID")
ENDPOINT_ID = os.getenv("ENDPOINT_ID")

aiplatform.init(project=PROJECT_ID, location=REGION)

RESOURCES_LINKS_PATH = "../dependencies/resource_links.json"
DOCUMENT_FOLDER = "resource-library"  
CHUNK_SIZE = 500  
CHUNK_OVERLAP = 50  
EMBEDDING_MODEL = VertexAIEmbeddings(model_name="text-embedding-005")

storage_client = storage.Client()

def download_pdfs(bucket_name, folder):
    """Download PDFs from the specified GCP bucket folder."""
    print("Downloading PDFs from GCP bucket...")
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=folder)

    local_files = []
    for blob in blobs:
        if blob.name.endswith(".pdf"):
            local_path = os.path.basename(blob.name)
            blob.download_to_filename(local_path)
            local_files.append(local_path)
            print(f"Downloaded {local_path}")

    return local_files

def get_pdf_links():
    """Load PDF links from the JSON file."""
    try:
        with open(RESOURCES_LINKS_PATH, "r", encoding="utf-8") as f:
            pdf_links = json.load(f)
        print("PDF links loaded successfully.")
        return pdf_links
    except FileNotFoundError:
        print(f"File not found: {RESOURCES_LINKS_PATH}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {RESOURCES_LINKS_PATH}: {e}")
        return {}

def preprocess_pdfs(pdf_files):
    """Preprocess PDFs to extract text chunks and metadata."""
    all_texts = []
    all_metadatas = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        is_separator_regex=False,
    )

    pdf_links = get_pdf_links()

    for file_name in pdf_files:
        print(f"Processing {file_name}...")
        loader = PyPDFLoader(file_name)
        pages = loader.load()

        doc_splits = text_splitter.split_documents(pages)

        texts = [doc.page_content for doc in doc_splits]
        metadatas = [
            {
                "file_name": file_name,
                "page_number": doc.metadata.get("page_number", None),
                "chunk_index": idx,
                "title": file_name.replace(".pdf", ""),
                "link": pdf_links.get(file_name, "Unknown"),
            }
            for idx, doc in enumerate(doc_splits)
        ]

        all_texts.extend(texts)
        all_metadatas.extend(metadatas)

    return all_texts, all_metadatas

def delete_local_files(file_paths):
    """Delete local files after processing."""
    print("Deleting local files...")
    for file_path in file_paths:
        try:
            os.remove(file_path)
            print(f"Deleted {file_path}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

class VectorSearch:
    """Vector Search class for managing the vector store."""

    def __init__(self, index_id, endpoint_id, embedding_model):
        self.vector_store = VectorSearchVectorStore.from_components(
            project_id=PROJECT_ID,
            region=REGION,
            gcs_bucket_name=BUCKET_NAME,
            index_id=index_id,
            endpoint_id=endpoint_id,
            embedding=embedding_model,
        )
        print("Vector store initialized.")

    def add_texts(self, texts, metadatas, is_complete_overwrite=True):
        """Add texts and metadata to the vector store."""
        print("Adding docs to vector store...")
        self.vector_store.add_texts(texts=texts, metadatas=metadatas, is_complete_overwrite=is_complete_overwrite)
        print("Docs added successfully.")

if __name__ == "__main__":
    
    #preprocess resources pdfs
    pdf_files = download_pdfs(BUCKET_NAME, DOCUMENT_FOLDER)
    texts, metadatas = preprocess_pdfs(pdf_files)
    delete_local_files(pdf_files)

    print(f"Processed {len(texts)} chunks.")
    print(f"Sample Text: {texts[0]}")
    print(f"Sample Metadata: {metadatas[0]}")

    # #create and update vector search
    EMBEDDING_MODEL = VertexAIEmbeddings(model_name="text-embedding-005")

    print("Creating vector store...")
    vector_search = VectorSearch(
        index_id=INDEX_ID, 
        endpoint_id=ENDPOINT_ID, 
        embedding_model=EMBEDDING_MODEL
        )
    print("Vector store created.")

    print("Updating vector store...")
    ## this can take over an hour
    # vector_search.add_texts(
    #     texts=texts, metadatas=metadatas, is_complete_overwrite=True)
    print("Vector store updated.")
