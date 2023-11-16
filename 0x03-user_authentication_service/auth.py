#!/usr/bin/env python3
"""
Hashed password
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> str:
        """
        Register a new user and returns the user obj
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError(f"User {email} already exists")
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(
                    email=email, hashed_password=hashed_password
            )
            return new_user
        except ValueError as ve:
            raise ve

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate login cedentials
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                password_bytes = password.encode('utf-8')
                hashed_password = user.hashed_password
                if bcrypt.checkpw(password_bytes, hashed_password):
                    return True
        except NoResultFound:
            return False
        return False


def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """
    Generate a str representation of a new uuid
    """
    return str(uuid.uuid4())
