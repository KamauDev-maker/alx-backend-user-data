#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth_type = getenv('AUTH_TYPE', 'auth')
if auth_type == 'auth':
    auth = Auth()

@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    unauthorized handler

    Args:
        error (_type_): _description_

    Returns:
        str: _description_
    """
    return jsonify({"error": "unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    forbidden handler

    Args:
        error (_type_): _description_

    Returns:
        str: _description_
    """
    return jsonify({"error": "forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.before_request
def authenticate_user():
    """authenticates user before request"""
    if auth:
        excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
        ]
        if auth.require_auth(request.path, excluded_paths):
            auth_header = auth.authorization_header(request)
            user = auth.current_user(request)
            if auth_header is None:
                abort(401)
            if user is None:
                abort(403)
    

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
