#!/usr/bin/env python3
"""Module containing DB model"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError, NoResultFound
from typing import Dict, Union

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self: User, email: str, hashed_password: str) -> User:
        """Saves a new user to the DB and returns the User Object"""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()

        return new_user

    def find_user_by(self, **kwargs: Dict) -> User:
        """Returns the first row found in the users
        table as filtered by the method’s input arguments """
        for key, value in kwargs.items():
            if value is None or not hasattr(User, key):
                raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs)\
            .first()
        if user:
            return user
        raise NoResultFound
