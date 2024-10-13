from flask import jsonify, request, make_response, session
from . import user_blueprint
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity, get_jwt
from datetime import timedelta


@user_blueprint.route('/profile', methods=['GET'])
@jwt_required()
def user_profile():
    claims = get_jwt()
    return jsonify(message=f"Welcome {session['username']} to the User Profile, your role is {claims['role']}"), 200

@user_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Simple example authentication check
    if username != 'admin' or password != 'password':
        return jsonify({"msg": "Bad username or password"}), 401

    # Store user info and login flag in session
    session['username'] = username
    session['user_logged_in'] = True  # Set user logged in flag to True
    user_role = "user"  # Example: assign role for user

    # Create access and refresh tokens with the role claim
    access_token = create_access_token(identity=username, additional_claims={"role": user_role})
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
