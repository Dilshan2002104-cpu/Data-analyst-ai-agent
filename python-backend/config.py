import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '../credentials/vertex-ai-key.json')
GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID', 'data-analyst-ai-agent-c0808')
GCP_LOCATION = os.getenv('GCP_LOCATION', 'us-central1')

# ChromaDB Configuration
CHROMADB_PERSIST_DIR = os.getenv('CHROMADB_PERSIST_DIR', './chromadb_data')

# Flask Configuration
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
PORT = int(os.getenv('PORT', 5000))

# Vertex AI Model Configuration
GEMINI_MODEL = 'gemini-2.0-flash-exp'
EMBEDDING_MODEL = 'text-embedding-004'

# Processing Configuration
MAX_CHUNK_SIZE = 1000  # Maximum rows per chunk for embedding
MAX_FILE_SIZE_MB = 50  # Maximum file size in MB
