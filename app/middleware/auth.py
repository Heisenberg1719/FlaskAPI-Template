from flask import request, jsonify, make_response, session
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, create_access_token, set_access_cookies, get_jwt
from datetime import timedelta

def jwt_required_middleware():
    allowed_paths = ['/user/login', '/admin/login', '/user/logout', '/admin/logout']
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

            # **Role-Based Access Control** for admin and user
            # Check for /admin path and require 'admin' role
            if '/admin' in request.path:
                # Extracting user role from JWT token
                if claims.get('role') != 'admin':
                    return jsonify({"msg": "Unauthorized!"}), 403  # Forbidden

                # Check session data for admin login status
                if 'admin_logged_in' not in session:
                    return jsonify({"msg": "Session expired or not logged in."}), 401  # Unauthorized

            # Check for /user path and require 'user' role
            if '/user' in request.path:
                # Extracting user role from JWT token
                if claims.get('role') != 'user':
                    return jsonify({"msg": "Unauthorized! User role required."}), 403  # Forbidden

                # Check session data for user login status
                if 'user_logged_in' not in session:
                    return jsonify({"msg": "Session expired or not logged in."}), 401  # Unauthorized

            # **Refresh Token Logic** (Optional)
            # Create a new access token to refresh expiration
            new_access_token = create_access_token(identity=current_user, additional_claims={"role": claims.get("role")}, expires_delta=timedelta(minutes=5))

            # Create the response and set the new access token in cookies
            response = make_response()
            set_access_cookies(response, new_access_token)

            # Return the response object (to update the cookie) or continue request processing
            return response  

        except Exception as e:
            # Handle token verification failure (e.g., missing or expired token)
            return jsonify({"msg": "Missing or invalid token"}), 401  # Unauthorized

    # If the request path is not protected, allow the request to proceed
    return None
