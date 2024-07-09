#!/usr/bin/env python3
"""Basic Auth Class"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """Basic Auth class inherits from Auth"""
    def extract_base64_authorization_header(self, authorization_header: str)\
            -> str:
        """Returns the Base64 part of the Authorization
        header for a Basic Authentication"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        auth_scheme, auth_params = authorization_header.split(' ', maxsplit=1)
        return auth_params
