#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth
from time import sleep

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

print("Testing create_session...")
sleep(2)

user_1 = auth.register_user(email, password)
session_id = auth.create_session(email)
print(f"user_1 sessiond_id: {session_id}")


user_2 = auth.register_user(email+"2", password)
session_id = auth.create_session(email+"2")
print(f"user_2 sessiond_id: {session_id}")


print(auth.create_session("unknown@email.com"))

print("Testing get_user_from_session_id...")
sleep(2)

session_id = (auth.create_session(email))
print(f"user from session_id: {session_id} is: {auth.get_user_from_session_id(session_id).id}")

print(auth.destroy_session(auth.get_user_from_session_id(auth.create_session(email)).id))
