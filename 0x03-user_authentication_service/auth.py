#!/usr/bin/env python3
"""Auth Module"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user
        """
        try:  # if user found, will raise an ValueError exception
            user = self._db.find_user_by(email=email)
            raise ValueError("User <user's email> already exists")
        except NoResultFound:
            user = self._db.add_user(email, (_hash_password(password)))
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate login
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str | None:
        """Finds a user and creates, saves and returns a session ID"""
        try:
            user = self._db.find_user_by(email=email)
            if user:  # case where user does not exists
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
            return None
        except NoResultFound:
            return None


def _hash_password(password: str) -> bytes:
    """Hash a password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a new UUID
    """
    return str(uuid.uuid4())
