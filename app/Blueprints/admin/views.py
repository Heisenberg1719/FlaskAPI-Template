from . import admin_blueprint
from datetime import datetime
from flask import jsonify, request, session
from flask_jwt_extended import (
jwt_required, create_access_token, create_refresh_token,
set_access_cookies, set_refresh_cookies, get_csrf_token)

class AdminRoutes:
    @staticmethod
    @admin_blueprint.route('/profile', methods=['GET'])
    @jwt_required()
    def admin_dashboard():
        return jsonify({"msg": "Welcome to the admin dashboard!"}), 200

    @staticmethod
    @admin_blueprint.route('/admin_login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'GET':
            phone_number = request.args.get('phone_number', None)
            if phone_number == '1234567890':
                username = 'admin'
            else:
                return jsonify({"msg": "Phone number not found"}), 404
            return jsonify({"username": username}), 200

        elif request.method == 'POST':
            username = request.json.get('username', None)
            password = request.json.get('password', None)

            if username != 'admin' or password != 'adminpassword':
                return jsonify({"msg": "Bad username or password"}), 401

            if session.get('admin_info') and session['admin_info'].get('username') == username:
                session.clear()

            session['admin_info'] = {
            'phone_number': username,'username': 'admin',
            'logged_in': True,'role': 'admin',
            'login_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

            access_token = create_access_token(identity='admin', additional_claims={"role": "admin"})
            refresh_token = create_refresh_token(identity='admin')

            response = jsonify({"msg": "Admin login successful"})
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)

            response.set_cookie('csrf_access_token', get_csrf_token(access_token), httponly=True, secure=True)
            response.set_cookie('csrf_refresh_token', get_csrf_token(refresh_token), httponly=True, secure=True)

            return response, 200

    @staticmethod
    @admin_blueprint.route('/logout', methods=['POST'])
    @jwt_required()
    def admin_logout():
        session.pop('admin_info', None)
        response = jsonify({"msg": "Admin logged out successfully"})
        response.set_cookie('access_token_cookie', '', expires=0, httponly=True, secure=True)
        response.set_cookie('refresh_token_cookie', '', expires=0, httponly=True, secure=True)
        response.set_cookie('csrf_access_token', '', expires=0, httponly=True, secure=True)
        response.set_cookie('csrf_refresh_token', '', expires=0, httponly=True, secure=True)
        return response, 200
