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
def auth_register(email, password, name_first, name_last):
    # Stage 1 - Validate input. 
    ah.validate_email(email)
    ah.validate_password(password)
    ah.validate_name_first(name_first)
    ah.validate_name_last(name_last)
    
    # Stage 2 - check database
    if dr.is_duplicate("email", email):
        raise InputError(description = 'Email address is already being used by another user')
    
    # Stage 3 - Generate input transformations
    token = ah.get_valid_token(email)
    u_id_returned = ah.get_u_id()
    
    # Stage 4 - Store all user information in the database
    db.add_user_to_database(email, \
        ah.hash_data(password), name_first, name_last, \
        ah.create_handle(name_first, name_last), \
        token, u_id_returned \
    )
    
    register_dict = {
        'u_id' : u_id_returned,
        'token' : token
    }
    return register_dict
     
        
def auth_login(email, password):
    return {
        'u_id': 1,
        'token': '12345',
    }

def auth_logout(token):
    return {
        'is_success': True,
    }
    
if __name__ == '__main__':
    pass
