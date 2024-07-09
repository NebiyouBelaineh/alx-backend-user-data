#!/usr/bin/env python3
"""Basic Auth Class"""
from api.v1.auth.auth import Auth
from typing import Tuple, TypeVar
from models.user import User
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

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str)\
            -> Tuple[str, str]:
        """Returns the user email and password from the
        Base64 decoded value."""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)

        email, pwd = decoded_base64_authorization_header.split(':', maxsplit=1)
        return (email, pwd)

    def user_object_from_credentials(self, user_email: str, user_pwd: str)\
            -> TypeVar('User'):
        """Returns the User instance based on his email and password."""
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        attributes = {'email': user_email}
        user = User.search(attributes)
        if len(user) == 0:
            return None
        if user[0].is_valid_password(user_pwd):
            return user[0]
        return None
