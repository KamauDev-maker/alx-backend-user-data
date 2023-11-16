#!/usr/bin/env python3
"""
Basic Flask app
"""
import logging
from flask import Flask, jsonify, abort, request
from auth import Auth

logging.disable(logging.WARNING)

AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    Get method returns a jsonify payload
    """
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user() -> str:
    """
    Endpoint to register a user
    """
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        new_user = AUTH.register_user(email, password)
        response = {
                "email": new_user.email,
                "message": "user created"
        }
        return jsonify(response)
    except ValueError as ve:
        response = {
                "message": "email already registered"
        }
        return jsonify(response), 400

@app.route("/session", methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    post session on logging
    """
    email, password = request.form.get("email"), request.form.get("password")
    if not Auth.valid_login(email, password):
        abort(401)
    session_id = Auth.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response

@app.route("sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    logout route to destroy the session
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
        AUTH.destroy_session(user.id)
        return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
