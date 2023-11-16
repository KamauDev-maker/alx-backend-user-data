#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify
from auth import Auth

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
        email = request.foam.get("email")
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
