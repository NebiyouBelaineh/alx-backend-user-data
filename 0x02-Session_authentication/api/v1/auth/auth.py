#!/usr/bin/env python3
"""Authentication Class"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Authentication Class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require_auth"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths or path + '/' in excluded_paths:
            return False
        for ex_path in excluded_paths:
            if ex_path.endswith('*'):
                wild_card_path, wild_card = ex_path.split('*')
                if path.startswith(wild_card_path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization_header"""
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """current_user"""
        return None

    def session_cookie(self, request=None) -> str:
        """Returns a cookie value (session_id) from a request based on
        the Environment variable SESSION_NAME"""
        if request is None:
            return None
        _my_session_id = os.getenv('SESSION_NAME')
        return request.cookies.get(_my_session_id)
