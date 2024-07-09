#!/usr/bin/env python3
"""Test require_auth in Auth class"""
from api.v1.auth.auth import Auth



auth = Auth()

excluded_paths = ["/api/v1/stat*"]
paths = ['/api/v1/users', '/api/v1/status', '/api/v1/stats']
for path in paths:
    print(auth.require_auth(path, excluded_paths))
