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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str)\
            -> str:
        """Returns the decoded value of a Base64
        string base64_authorization_header"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            if len(base64_authorization_header) % 4 != 0:
                raise Exception
            auth_header = base64.b64decode(base64_authorization_header,
                                           validate=True)
            return auth_header.decode('utf-8')
        except Exception:
            return None
