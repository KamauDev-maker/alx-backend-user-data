#!/usr/bin/env python3
"""
Basic auth
"""
import re
import base64
import binascii
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


def decode_base64_authorization_header(
    self,
    base64_authorization_header: str
) -> str:
    """"a method that decodes value base64string"""
    if type(base64_authorization_header) == str:
        try:
            result = base64.b64decode(
                extract_base64_authorization_header,
                validate=True,
            )
            return result.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None
