"""
 auth.py
# This function takes in input from the user, validates it, checks against the database, then authenticates them if everything is correct.

"""
# Usage
    # Used for Validation of input only. 

# Additions:
# 21/03/20
    # - register finished

from error import AccessError, InputError
import database_files.database_update as du
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
    return {
        'u_id': 1,
        'token': '12345',
    }     
 
        
def auth_login(email, password):
    # Validate Email
    ah.validate_email(email)
    user_rec =  dr.get_users_by_key("email", email)
    print(user_rec)
    if user_rec == []:
        raise InputError(description = 'Email entered does not belong to a user')
    
    # Validate Password
    hash_pw = ah.hash_data(password)
    if hash_pw != user_rec[0]["password"]:
        raise InputError(description = 'Password is not correct')

    # Create and assign token to database
    # new_token = ah.get_valid_token(email)
    login_dict = du.login_user(email)

    return login_dict
        
def auth_logout(token):
    return {
        'is_success': True,
    }

if __name__ == '__main__':
    pass
