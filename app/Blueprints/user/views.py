from flask import jsonify, request, make_response
from . import user_blueprint 
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity, get_jwt


@user_blueprint.route('/profile', methods=['GET'])
@jwt_required()
def user_profile():
    claims = get_jwt()
    return jsonify(message=f"Welcome to the User Profile, your role is {claims['role']}"), 200

@user_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    # Simple example authentication check
    if username != 'admin' or password != 'password':  
        return jsonify({"msg": "Bad username or password"}), 401

    # Create access and refresh tokens with the role claim
    access_token = create_access_token(identity=username, additional_claims={"role": "user"})
    refresh_token = create_refresh_token(identity=username)

    # Create the response object
    response = jsonify({"msg": "User login successful"})
    response.set_cookie('access_token_cookie', access_token, httponly=True, secure=True)
    response.set_cookie('refresh_token_cookie', refresh_token, httponly=True, secure=True)
    return response, 200
