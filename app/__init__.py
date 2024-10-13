from flask import Flask
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_cors import CORS  # Import CORS
from app.Blueprints.admin import admin_blueprint
from app.Blueprints.user import user_blueprint
from app.Blueprints.public import public_blueprint
from app.middleware.auth import jwt_required_middleware

def create_app(config_class):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    app.config.from_pyfile('config.py', silent=True) 
    # Initialize JWT, CSRF, Session, and CORS
    jwt = JWTManager(app)
    csrf = CSRFProtect(app)
    Session(app)
    # Initialize CORS
    CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all domains (in production, restrict this)
    # Register Blueprints
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(public_blueprint)
    # Register middleware
    app.before_request(jwt_required_middleware)
    return app
