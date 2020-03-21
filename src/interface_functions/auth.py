"""
 auth.py
# This function takes in input from the user, validates it, checks against the database, then authenticates them if everything is correct.

"""
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
    if dr.is_duplicate_check("email", email):
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
    # Validate Email
    ah.validate_email(email)
    user_rec =  dr.get_users_by_key("email", email)
    if user_rec == []:
        raise InputError(description = 'Email entered does not belong to a user')
    
    # Validate Password
    hash_pw = ah.hash_data(password)
    if hash_pw != user_rec[0]["password"]:
        raise InputError(description = 'Password is not correct')

    # Create and assign token to database
    new_token = ah.get_valid_token(email)
    login_dict = db.login_user(email, new_token)

    return login_dict
        
        
def auth_logout(token):
    return {
        'is_success': True,
    }

    
if __name__ == '__main__':
    pass
