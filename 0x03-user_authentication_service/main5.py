#!/usr/bin/env python3
"""
Main file
"""
from auth import _hash_password, _generate_uuid

print(_hash_password("Hello Holberton"))
print(type(_hash_password("Hello Holberton")))

print(_generate_uuid())
