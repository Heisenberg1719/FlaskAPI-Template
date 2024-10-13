import logging
from flask_jwt_extended import *
from flask import request, jsonify ,make_response
from datetime import timedelta


def jwt_required_middleware():
    allowed_paths = ['/', '/user/login', '/admin/admin_login', '/user/logout', '/admin/logout']
    if request.path not in allowed_paths:
        try:
            verify_jwt_in_request()
            current_user,claims = get_jwt_identity(), get_jwt()
            if "user" in request.path and claims.get('role') == "user":pass
            elif "admin" in request.path and claims.get('role') == "admin":pass
            else:
                logging.warning(f"Unauthorized role access attempt by '{current_user}'. Path: {request.path}")
                return jsonify({"msg": "Unauthorized role access"}), 403

            new_access_token = create_access_token(identity=current_user,additional_claims={"role": claims.get("role")},expires_delta=timedelta(minutes=5))
            set_access_cookies(response, new_access_token)
            return response
        except Exception as e:
            logging.error(f"Error during JWT verification: {str(e)}", exc_info=True)
            request.jwt_verification_failed = True

    return None  # Continue processing the request
