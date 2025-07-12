import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory of the application
BASE_DIR = Path(__file__).parent
INSTANCE_DIR = BASE_DIR / 'instance'
LOGS_DIR = BASE_DIR / 'logs'

# Create required directories if they don't exist
os.makedirs(INSTANCE_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

class Config:
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123')
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    FLASK_APP = os.getenv('FLASK_APP', 'app.py')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{str(INSTANCE_DIR / "ecommerce.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Application settings
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '5000'))
    
    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', str(LOGS_DIR / 'app.log'))
    LOG_ROTATION = os.getenv('LOG_ROTATION', '10 MB')
    LOG_RETENTION = os.getenv('LOG_RETENTION', '30 days')
    
    # Application settings
    ITEMS_PER_PAGE = int(os.getenv('ITEMS_PER_PAGE', '12'))
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', str(BASE_DIR / 'static' / 'uploads'))
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', str(16 * 1024 * 1024)))  # 16MB
    
    # Create upload folder if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    @classmethod
    def init_app(cls, app):
        """Initialize configuration for the Flask app"""
        # Ensure all paths are absolute
        app.config['UPLOAD_FOLDER'] = os.path.abspath(cls.UPLOAD_FOLDER)
        
        # Create upload folder if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
