import logging
from flask_cors import CORS
from flask_session import Session
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from app.Blueprints.user import user_blueprint
from app.Blueprints.admin import admin_blueprint
from logging.handlers import RotatingFileHandler
from app.Blueprints.public import public_blueprint
from app.middleware.auth import jwt_required_middleware

def create_app(config_class):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    app.config.from_pyfile('config.py', silent=True)
    jwt = JWTManager(app)# Initialize extensions
    Session(app)
    CORS(app, resources={r"/*": {"origins": "*"}})
    # Register Blueprints
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(public_blueprint)
    app.before_request(jwt_required_middleware)
    setup_logging(app)

    # Log errors and critical issues only
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Error occurred: {str(e)}", exc_info=True)
        return jsonify({"msg": "An error occurred"}), 500

    return app

def setup_logging(app):
    # Set the log level to WARNING for capturing only important issues
    app.logger.setLevel(logging.WARNING)  # Only WARNING and higher (ERROR, CRITICAL)

    # Create a file handler to log to a file with rotation
    file_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=10)
    # file_handler.setLevel(logging.WARNING)  # Log only WARNING, ERROR, CRITICAL to file

    # Define a simplified log format (no path or line number)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    file_handler.setFormatter(formatter)

    # Add handler to the app logger
    app.logger.addHandler(file_handler)

    # Log a message to confirm that logging is set up
    # app.logger.warning("Logging setup complete: Only warnings, errors, and critical issues will be logged.")

