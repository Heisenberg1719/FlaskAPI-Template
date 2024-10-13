from flask import request, jsonify, make_response
from flask_jwt_extended import (
    verify_jwt_in_request, get_jwt_identity, 
    create_access_token, set_access_cookies, get_jwt
)
from functools import wraps
from datetime import timedelta

def jwt_required(role=None):
    """Decorator to enforce JWT authentication and role-based access control."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            allowed_paths = ['/user/login', '/admin/admin_login', '/user/logout', '/admin/logout']

            # Check if the current path is in the allowed paths where JWT is not required
            if request.path in allowed_paths:
                return fn(*args, **kwargs)  # Skip JWT verification for these paths

            try:
                # Verify JWT token in the request
                verify_jwt_in_request()

                # Get the current user's identity and claims (including the role)
                current_user = get_jwt_identity()
                claims = get_jwt()

                # Role-Based Access Control
                if role and claims.get('role') != role:
                    return jsonify({"msg": f"Unauthorized! {role} role required."}), 403  # Forbidden

                # **Optional Refresh Token Logic**
                # Create a new access token to refresh expiration
                new_access_token = create_access_token(
                    identity=current_user,
                    additional_claims={"role": claims.get("role")},
                    expires_delta=timedelta(minutes=5)
                )

                # Call the original route handler and get the response and status code
                response, status_code = fn(*args, **kwargs)

                # Create the response and set the new access token in cookies
                response = make_response(response, status_code)
                set_access_cookies(response, new_access_token)

                return response  # Return the updated response

            except KeyError as e:
                return jsonify({"msg": "Missing required data", "error": str(e)}), 400

            except AttributeError as e:
                return jsonify({"msg": "Invalid attribute or data", "error": str(e)}), 400

            except Exception as e:
                return jsonify({"msg": "Missing or invalid token", "error": str(e)}), 401

        return wrapper
    return decorator
