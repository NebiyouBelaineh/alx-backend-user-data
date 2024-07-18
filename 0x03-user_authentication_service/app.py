#!/usr/bin/env python3
"""Flask app"""
from flask import Flask, jsonify, Response, request, abort
from auth import Auth
from typing import Union, Tuple

app = Flask(__name__)
AUTH = Auth()


@app.route("/", strict_slashes=False)
def home() -> Response:
    """Returns JSON Payload"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> Union[Response, Tuple[Response, int]]:
    """Gets email and password from the form and checks if it's valid
    and registers it if it does not exist"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)  # type: ignore
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> Union[Response, Tuple[Response, int]]:  # type: ignore
    """Checks email and password and creates session ID and returns
    a JSON payload with the 'session_id' set as a cookie in the
    response object"""
    email, pwd = request.form.get("email"), request.form.get("password")
    user_exists = AUTH.valid_login(email, pwd)  # type: ignore
    if not user_exists:
        abort(401)
    session_id = AUTH.create_session(email)  # type: ignore
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)  # type: ignore
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)  # type: ignore
