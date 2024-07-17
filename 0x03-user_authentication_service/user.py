#!/usr/bin/env python3
"""Module containing User model, an SQLALCHEMY model"""
from sqlalchemy import Column, Integer, String


class User:
    """User Model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
