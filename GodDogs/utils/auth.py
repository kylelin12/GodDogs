import os, hashlib
from flask import session
import database

# Creates a new user
def new_user(u, p):
    return database.add_user(u, encrypt(p))

# Change password for user
def update_pw(u, p):
    return database.change_pw(u, encrypt(p))

# Encrypt passwords
def encrypt(p):
    return hashlib.sha224(p.encode('utf-8')).hexdigest()

# Checks password
def pw_verify(u, p):
    return encrypt(p) == database.check_pass(u)

# Checks username
def u_exists(u):
    return database.check_pass(u) is not None

# Logged in checker
def logged_in():
    return 'username' in session

# Creates a new session if username and password match
def login(u, p):
    if(pw_verify(u, p)):
        session['username'] = username
        return True
    else:
        return False

# Logs out
def logout():
    if logged_in():
        session.pop('username')