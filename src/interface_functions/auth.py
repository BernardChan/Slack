"""
 auth.py
# This function takes in input from the user, validates it, checks against the database, then authenticates them if everything is correct.

"""
# Usage
    # Used for Validation of input only. 

# Additions:
# 21/03/20
    # - register finished
# 23/03/20
    # - Login and Logout

from error import AccessError, InputError
import database_files.database as db
import database_files.database_retrieval as dr
import helper_functions.auth_helper as ah
import pytest
import time

"""
----------------------------------------------------------------------------------
User Interface Functions
----------------------------------------------------------------------------------
"""     
def auth_login(email, password):
    return {
        'u_id': 1,
        'token': '12345',
    }

def auth_logout(token):
    is_success = db.logout_user(token)
    return is_success

def auth_register(email, password, name_first, name_last):
    return {
        'u_id': 1,
        'token': '12345',
    }
