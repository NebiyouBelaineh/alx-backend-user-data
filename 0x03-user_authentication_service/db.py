#!/usr/bin/env python3
"""Module containing DB model"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict, Union, Optional

from user import Base, User  # type: ignore


class DB:
    """DB class
    """
    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)  # type: ignore
        Base.metadata.create_all(self._engine)  # type: ignore
        self.__session: Optional[Session] = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Saves a new user to the DB and returns the User Object"""
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()

        return new_user

    def find_user_by(self, **kwargs: Union[str, int]) -> User:
        """Returns the first row found in the users
        table as filtered by the method’s input arguments """
        session = self._session

        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError()

        result = session.query(User).filter_by(**kwargs).first()
        if result is None:
            raise NoResultFound()
        return result

    def update_user(self, user_id: int, **kwargs: Union[str, int]) -> None:
        """Updates a user instance attributes based on its ID"""
        session = self._session

        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise ValueError()
            setattr(user, key, value)
        session = self._session
        session.add(user)
        session.commit()
