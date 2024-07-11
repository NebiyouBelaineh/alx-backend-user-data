#!/usr/bin/env python3
""" Module for views for Session Authentication"""

from api.v1.views import app_views
from flask import abort, request, jsonify
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Takes in user email and password and creates and
    returns a dictionary of the User
    Otherwise, returns a corosponding error message inside a JSON"""
    email, pwd = request.form.get('email'), request.form.get('password')

    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if pwd is None or pwd == '':
        return jsonify({"error": "password missing"}), 400

    try:
        user_list = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(user_list) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = user_list[0]
    if not user.is_valid_password(pwd):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    cookie_name = os.getenv('SESSION_NAME')

    response.set_cookie(cookie_name, session_id)
    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def view_session_auth_logout() -> str:
    """ DELETE /api/v1/auth_session/logout """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
