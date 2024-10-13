from flask import jsonify, request, session
from . import admin_blueprint  # Import the admin blueprint from the same folder
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, get_jwt_identity, get_jwt
from datetime import timedelta

# Admin profile route that checks the role and requires JWT authentication
@admin_blueprint.route('/admin_profile', methods=['GET'])
@jwt_required()
def admin_profile():
    # Extracting user role from JWT token
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"msg": "Admins only!"}), 403
    
    # Check session data (optional)
    if 'admin_logged_in' not in session:
        return jsonify({"msg": "Session expired or not logged in."}), 401
    
    return jsonify(message=f"Welcome to the Admin Profile, your role is {claims['role']}"), 200

# Admin login route
@admin_blueprint.route('/admin_login', methods=['POST'])
def admin_login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    # Simple example authentication check for admin
    if username != 'admin' or password != 'adminpassword':
        return jsonify({"msg": "Bad username or password"}), 401

    # Create access and refresh tokens with the role claim
    access_token = create_access_token(identity=username, additional_claims={"role": "admin"})
    refresh_token = create_refresh_token(identity=username)
    response = jsonify({"msg": "Admin login successful"})
    response.set_cookie('access_token_cookie', access_token, httponly=True, secure=True)
    response.set_cookie('refresh_token_cookie', refresh_token, httponly=True, secure=True)
    session['admin_logged_in'] = True
    session['username'] = username
    return response, 200
