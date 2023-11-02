#!/usr/bin/env python3
"""
returns a salted, hashed password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate a plaintext password
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    except ValueError:
        return False
