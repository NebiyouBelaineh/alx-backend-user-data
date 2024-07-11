#!/usr/bin/env python3
""" Session Auth Class
"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ Session Auth Class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates and returns a session ID for a user_id.
        """
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID"""
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value"""
        if request is None:
            return None

        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        user_instance = User.get(user_id)
        return user_instance
