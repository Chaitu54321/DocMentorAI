import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Base directory paths
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
CHROMA_PATH = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")

# Embedding model settings
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "BAAI/bge-small-en-v1.5")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "docmentor")

# Future milestones (Groq API Key)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
