from flask import request, jsonify, make_response
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, create_access_token, set_access_cookies, get_jwt
from datetime import timedelta

def jwt_required_middleware():
    # List of endpoints that don't require JWT
    allowed_paths = ['/user/login', '/admin/login']

    # Skip JWT verification for allowed paths
    if request.path in allowed_paths:
        return None  # Proceed without JWT verification

    # Check if the path is not the base URL ("/")
    if request.path != '/':
        try:
            # Verify JWT token in the request
            verify_jwt_in_request()

            # Get the current user's identity and claims (including the role)
            current_user = get_jwt_identity()
            claims = get_jwt()

            # Check for /admin path and require 'admin' role
            if '/admin' in request.path and claims.get('role') != 'admin':
                return jsonify({"msg": "Unauthorized"}), 403  # Forbidden

            # Check for /user path and require 'user' role
            if '/user' in request.path and claims.get('role') != 'user':
                return jsonify({"msg": "Unauthorized!"}), 403  # Forbidden

            # Refresh token expiration by creating a new access token
            new_access_token = create_access_token(identity=current_user, additional_claims={"role": claims.get("role")}, expires_delta=timedelta(minutes=5))

            # Create the response and set the new access token in cookies
            response = make_response()
            set_access_cookies(response, new_access_token)
            
            return response  
        except Exception as e:
            return jsonify({"msg": "Missing or invalid token"}), 401

    return None  
