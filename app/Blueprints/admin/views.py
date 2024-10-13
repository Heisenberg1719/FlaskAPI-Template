from flask import jsonify, request
from . import admin_blueprint  # Import the admin blueprint from the same folder
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, get_jwt_identity, get_jwt

@admin_blueprint.route('/admin_profile', methods=['GET'])
@jwt_required()
def admin_profile():
    # Extracting user role from JWT token
    claims = get_jwt()
    if claims['role'] != 'admin':
        return jsonify({"msg": "Admins only!"}), 403
    return jsonify(message=f"Welcome to the Admin Profile, your role is {claims['role']}"), 200

@admin_blueprint.route('/admin_login', methods=['POST'])
def admin_login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    if username != 'admin' or password != 'adminpassword':  # Example authentication for admin
        return jsonify({"msg": "Bad username or password"}), 401

    # Create access and refresh tokens with the role claim,set the JWT tokens in HttpOnly cookies in one line
    access_token = create_access_token(identity=username, additional_claims={"role": "admin"})
    refresh_token = create_refresh_token(identity=username)
    # Create the response object
    response = jsonify({"msg": "Admin login successful"})
    response.set_cookie('access_token_cookie', access_token, httponly=True, secure=True)
    response.set_cookie('refresh_token_cookie', refresh_token, httponly=True, secure=True)
    return response, 200

