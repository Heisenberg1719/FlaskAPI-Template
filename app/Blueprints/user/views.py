from flask import jsonify, request, make_response, session
from . import user_blueprint
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity, get_jwt
from datetime import timedelta,datetime


@user_blueprint.route('/user/profile', methods=['GET'])
@jwt_required(role='user')
def user_profile():
    # Example of returning response and status code
    return jsonify({"msg": "Welcome to your profile!"}), 200



@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Handle GET request - Retrieve the username based on phone number
        phone_number = request.args.get('phone_number', None)
        
        # Example: Mocking a database lookup for username by phone number
        if phone_number == '1234567890':  # Replace with actual DB logic
            username = 'admin'
        else:
            return jsonify({"msg": "Phone number not found"}), 404
        
        return jsonify({"username": username}), 200

    elif request.method == 'POST':
        # Handle POST request - Login the user
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        # Simple example authentication check
        if username != 'admin' or password != 'password':  # Replace with actual authentication logic
            return jsonify({"msg": "Bad username or password"}), 401

        # Check if the user has an active session and revoke it
        if session.get('user_info') and session['user_info'].get('username') == username:
            # Revoke the previous session by clearing session data
            session.clear()
            print(f"Revoked previous session for user: {username}")

        # Create new session info
        session['user_info'] = {
            'username': username,
            'logged_in': True,  # Set user logged in flag to True
            'role': 'user',  # Store user role
            'login_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')  # Store login time
        }

        # Create access and refresh tokens with the role claim
        access_token = create_access_token(identity=username, additional_claims={"role": "user"})
        refresh_token = create_refresh_token(identity=username)

        # Create the response object
        response = jsonify({"msg": "User login successful"})
        
        # Set access and refresh tokens in HttpOnly cookies
        response.set_cookie('access_token_cookie', access_token, httponly=True, secure=True)
        response.set_cookie('refresh_token_cookie', refresh_token, httponly=True, secure=True)

        return response, 200

@user_blueprint.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Clear session and cookies on logout
    session.pop('username', None)
    session.pop('user_logged_in', None)  # Clear the user_logged_in flag
    
    response = jsonify({"msg": "User logged out successfully"})
    response.set_cookie('access_token_cookie', '', expires=0, httponly=True, secure=True)
    response.set_cookie('refresh_token_cookie', '', expires=0, httponly=True, secure=True)
    response.set_cookie('csrf_access_token', '', expires=0, httponly=False, secure=True)  
    return response, 200
