#!/usr/bin/env python3
"""Session authentication
"""
from uuid import uuid4
from models.user import User
from .auth import Auth


class SessionAuth(Auth):
    """
    Session authentication class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id.
        """
        if type(user_id) is str:
            session_id = str(uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        
    def user_id_by_session_id(self, session_id: str=None) -> str:
        """"Retrieves user Id"""
        if type(session_id) is str:
            return self.user_id_by_session_id.get(session_id)
        
    def current_user(self, request=None) -> User:
        """"Returns the current user"""
        session_id = self.session_cookie(request)
        user = User.get(user_id)
        return user
        
