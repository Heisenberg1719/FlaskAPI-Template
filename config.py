import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your-jwt-secret-key'
    
    # Session configuration
    SESSION_TYPE = 'filesystem'  
    SESSION_PERMANENT = False
    
    # JWT Configuration
    JWT_TOKEN_LOCATION = ['cookies']  # Store JWT in cookies
    JWT_COOKIE_CSRF_PROTECT = True  # Enable CSRF protection for JWT cookies
    JWT_ACCESS_COOKIE_HTTPONLY = True  # HttpOnly flag to prevent XSS
    JWT_REFRESH_COOKIE_HTTPONLY = True
    JWT_COOKIE_SECURE = True  # Set to True for HTTPS in production
    
    # Token expiration times
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)  # Access token expires in 5 minutes
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=15)  # Refresh token expires in 15 minutes

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False  # Disable secure cookie for development
    JWT_COOKIE_SECURE = False  # Disable secure cookies for local dev (HTTP)

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True  # Secure cookie for HTTPS in production
    JWT_COOKIE_SECURE = True  # Enable secure cookies for HTTPS in production
