import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'c498444b7a980f814dc985968f239a9bc3aa93cdb9f870cde99ad58f84a5f267'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    
    # Rate limiting settings
    RATELIMIT_DEFAULT = "100 per minute"
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL') or "memory://"
    
    # Caching settings
    CACHE_TYPE = "simple"  # Use Redis in production
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    CACHE_KEY_PREFIX = "mindflow_"
    
    # CORS settings
    CORS_ORIGINS = ["*"]  # Configure properly in production
    CORS_SUPPORTS_CREDENTIALS = True
    CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    
    # API settings
    API_TITLE = "MindFlow API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "MindFlow Game Backend API"
    
    # Mobile optimization settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = "uploads"
    
    # Pagination settings
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # Security settings
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Performance settings
    THREADED = True
    USE_RELOADER = True

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True
    
    # Development rate limits (more permissive)
    RATELIMIT_DEFAULT = "200 per minute"
    
    # Development caching (faster refresh)
    CACHE_DEFAULT_TIMEOUT = 60  # 1 minute

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Production security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    
    # Production rate limits (more restrictive)
    RATELIMIT_DEFAULT = "50 per minute"
    
    # Production caching (longer cache)
    CACHE_DEFAULT_TIMEOUT = 600  # 10 minutes
    
    # Use Redis for caching and rate limiting
    CACHE_TYPE = "redis"
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL')

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    
    # Testing rate limits (very permissive)
    RATELIMIT_DEFAULT = "1000 per minute"
    
    # Testing caching (no cache)
    CACHE_TYPE = "null"

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default']) 