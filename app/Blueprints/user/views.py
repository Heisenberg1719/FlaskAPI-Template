from . import user_blueprint
from datetime import datetime
from flask import jsonify, request, session
from flask_jwt_extended import (
jwt_required, create_access_token, create_refresh_token,
set_access_cookies, set_refresh_cookies, get_csrf_token)

class UserRoutes:
    @staticmethod
    @user_blueprint.route('/profile', methods=['GET'])
    @jwt_required()
    def user_profile():
        return jsonify("Welcome from userpanel home"), 200

    @staticmethod
    @user_blueprint.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            phone_number = request.args.get('phone_number', None)
            if phone_number == '1234567890':username = 'admin'
            else:return jsonify({"msg": "Phone number not found"}), 404
            return jsonify({"username": username}), 200

        elif request.method == 'POST':
            username = request.json.get('username', None)
            password = request.json.get('password', None)
            if username != 'admin' or password != 'adminpassword':
                return jsonify({"msg": "Bad username or password"}), 401
            if session.get('user_info') and session['user_info'].get('username') == username:session.clear()
            session['user_info'] = {'username': username,'logged_in': True,
            'role': 'user','login_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            access_token = create_access_token(identity=username, additional_claims={"role": "user"})
            refresh_token = create_refresh_token(identity=username)
            response = jsonify({"msg": "User login successful"})
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            response.set_cookie('csrf_access_token', get_csrf_token(access_token), httponly=True, secure=True)
            response.set_cookie('csrf_refresh_token', get_csrf_token(refresh_token), httponly=True, secure=True)
            return response, 200


    @staticmethod
    @user_blueprint.route('/logout', methods=['POST'])
    @jwt_required()
    def logout():
        [session.pop(key, None) for key in ['username', 'user_logged_in', 'user_info']]
        response = jsonify({"msg": "User logged out successfully"})
        cookies_to_clear = ['access_token_cookie', 'refresh_token_cookie', 'csrf_access_token', 'csrf_refresh_token']
        for cookie in cookies_to_clear:response.set_cookie(cookie, '', expires=0, httponly=True, secure=True)
        return response, 200
