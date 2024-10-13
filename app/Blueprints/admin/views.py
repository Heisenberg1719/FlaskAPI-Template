from flask import jsonify, request, session
from . import admin_blueprint  # Import the admin blueprint from the same folder
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, get_jwt_identity, get_jwt
from datetime import timedelta

# Admin profile route that checks the role and requires JWT authentication
@admin_blueprint.route('/admin/profile', methods=['GET'])
@jwt_required(role='admin')
def admin_dashboard():
    return jsonify({"msg": "Welcome to the admin dashboard!"}), 200


@admin_blueprint.route('/admin_login', methods=['GET', 'POST']) # Admin login route
def admin_login():
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
        # Handle POST request - Login the admin
        phone_number = request.json.get('phone_number', None)
        password = request.json.get('password', None)

        # Example: Mocking a database lookup for phone number and password authentication
        if phone_number != '1234567890' or password != 'adminpassword':  # Replace with actual authentication logic
            return jsonify({"msg": "Bad phone number or password"}), 401

        # Check if the admin has an active session and revoke it
        if session.get('admin_info') and session['admin_info'].get('phone_number') == phone_number:
            # Revoke the previous session by clearing session data
            session.clear()
            print(f"Revoked previous session for admin with phone number: {phone_number}")

        # Store new session info for the admin
        session['admin_info'] = {
            'phone_number': phone_number,
            'username': 'admin',
            'logged_in': True,  # Set admin logged in flag to True
            'role': 'admin',  # Store admin role
            'login_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')  # Store login time
        }

        # Create access and refresh tokens with the role claim
        access_token = create_access_token(identity='admin', additional_claims={"role": "admin"})
        refresh_token = create_refresh_token(identity='admin')

        # Create the response object
        response = jsonify({"msg": "Admin login successful"})
        
        # Set access and refresh tokens in HttpOnly cookies
        response.set_cookie('access_token_cookie', access_token, httponly=True, secure=True)
        response.set_cookie('refresh_token_cookie', refresh_token, httponly=True, secure=True)
        return response, 200
