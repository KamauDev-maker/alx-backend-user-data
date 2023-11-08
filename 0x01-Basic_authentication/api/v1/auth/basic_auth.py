#!/usr/bin/env python3
"""
Basic auth
"""
import re
from .auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    basic auth class
    """
    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """Extracts the authorization header"""
        if type(authorization_header) == str:
            pattern = r'Basic(?P<token>.+)'
            field_match = re.fullmatch(pattern, authorization_header.strip())
            if field_match is not None:
                return field_match.group('token')
        return None
