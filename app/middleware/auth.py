import logging
from flask_jwt_extended import (
    verify_jwt_in_request, get_jwt_identity, get_jwt, create_access_token
)
from flask import request, jsonify
from datetime import timedelta

def jwt_required_middleware():
    allowed_paths = ['/', '/user/login', '/admin/admin_login', '/user/logout', '/admin/logout']
    
    if request.path not in allowed_paths:
        try:
            # Verify JWT token
            verify_jwt_in_request()
            current_user, claims = get_jwt_identity(), get_jwt()

            # Role-based access control
            if "user" in request.path and claims.get('role') == "user":
                pass
            elif "admin" in request.path and claims.get('role') == "admin":
                pass
            else:
                logging.warning(f"Unauthorized role access attempt by '{current_user}'. Path: {request.path}")
                return jsonify({"msg": "Unauthorized role access"}), 403

            # Create a new access token for refresh purposes
            new_access_token = create_access_token(
                identity=current_user,
                additional_claims={"role": claims.get("role")},
                expires_delta=timedelta(minutes=5)
            )
            # Attach new token to the request context so the route can use it
            request.new_access_token = new_access_token

        except KeyError as e:
            # Handle missing role or unexpected claims
            logging.error(f"KeyError during JWT verification: Missing key - {str(e)}", exc_info=True)
            return jsonify({"msg": "Token verification failed. Missing required information.", "error": str(e)}), 400

        except AttributeError as e:
            # Handle missing or incorrect attributes in the token
            logging.error(f"AttributeError during JWT verification: {str(e)}", exc_info=True)
            return jsonify({"msg": "Invalid token attributes.", "error": str(e)}), 400

        except Exception as e:
            # Generic exception handling for unforeseen issues
            logging.error(f"Error during JWT verification: {str(e)}", exc_info=True)
            request.jwt_verification_failed = True

    return None  # Continue processing the request
