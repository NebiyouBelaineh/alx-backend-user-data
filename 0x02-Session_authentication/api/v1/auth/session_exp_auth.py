#!/usr/bin/env python3
"""SessionExpAuth Class Module"""

from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Class to add Expiration date to a Session ID"""
    def __init__(self):
        """Initializer"""
        session_duration = os.getenv('SESSION_DURATION')
        if session_duration is None:
            self.session_duration = 0
        try:
            self.session_duration = int(session_duration)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Creates and returns a session ID for a user_id."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID from session_dictionary"""
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration == 0:
            return self.user_id_by_session_id[session_id].get('user_id')
        if self.user_id_by_session_id[session_id].get('created_at') is None:
            return None
        if self.user_id_by_session_id[session_id].get('created_at') + \
                timedelta(seconds=self.session_duration) < datetime.now():
            return None
        return self.user_id_by_session_id[session_id].get('user_id')
