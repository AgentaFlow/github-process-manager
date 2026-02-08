"""
Configuration module for the RAG Chatbot.
Loads and validates environment variables.
"""
import os
from dotenv import load_dotenv
from logger import logger

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class."""
    
    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # GitHub Configuration
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    GITHUB_REPO_URL = os.getenv('GITHUB_REPO_URL', '')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    ENV = os.getenv('FLASK_ENV', 'development')
    
    # ChromaDB Configuration
    CHROMA_DB_PATH = os.getenv('CHROMA_DB_PATH', './chroma_db')
    
    # Upload Configuration
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'app.log')
    
    # RAG Configuration
    CHUNK_SIZE = 800  # Characters per chunk
    CHUNK_OVERLAP = 200  # Overlap between chunks
    TOP_K_RESULTS = 3  # Number of relevant chunks to retrieve
    
    # Gemini Model Configuration
    GEMINI_MODEL = 'gemini-2.5-flash'  # Latest stable Gemini 2.5 Flash model
    GEMINI_EMBEDDING_MODEL = 'models/text-embedding-004'
    TEMPERATURE = 0.7
    MAX_OUTPUT_TOKENS = 2048
    
    @staticmethod
    def validate():
        """Validate critical configuration settings."""
        errors = []
        
        if not Config.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY is not set. Please add it to your .env file.")
        
        if not Config.GITHUB_TOKEN:
            logger.warning("GITHUB_TOKEN is not set. GitHub features will be limited.")
        
        if not Config.GITHUB_REPO_URL:
            logger.warning("GITHUB_REPO_URL is not set. Please configure it to use GitHub features.")
        
        if errors:
            error_msg = "\n".join(errors)
            logger.error(f"Configuration validation failed:\n{error_msg}")
            raise ValueError(f"Configuration errors:\n{error_msg}")
        
        # Create necessary directories
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.CHROMA_DB_PATH, exist_ok=True)
        
        logger.info("Configuration validated successfully")
        return True

    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed."""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
