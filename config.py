import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ai-admonitor-secret-key-2026-prod'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'database', 'admonitor.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Google Ads Configuration
    GOOGLE_ADS_DEVELOPER_TOKEN = os.environ.get('GOOGLE_ADS_DEVELOPER_TOKEN', '')
    GOOGLE_ADS_CLIENT_ID = os.environ.get('GOOGLE_ADS_CLIENT_ID', '')
    GOOGLE_ADS_CLIENT_SECRET = os.environ.get('GOOGLE_ADS_CLIENT_SECRET', '')
    GOOGLE_ADS_REFRESH_TOKEN = os.environ.get('GOOGLE_ADS_REFRESH_TOKEN', '')
    GOOGLE_ADS_CUSTOMER_ID = os.environ.get('GOOGLE_ADS_CUSTOMER_ID', '')
    
    # Platform Mode (Demo Mode enabled by default if no credentials provided)
    DEMO_MODE_DEFAULT = True
    
    # Models directory
    MODELS_DIR = os.path.join(BASE_DIR, 'models')
    DATASETS_DIR = os.path.join(BASE_DIR, 'datasets')
