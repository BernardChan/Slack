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
import database_files.database_update as du
import database_files.database_retrieval as dr
import helper_functions.auth_helper as ah
import helper_functions.interface_function_helpers as help
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

    # Stage 4 - Store all user information in the database
    u_id_returned = help.get_unique_id()
    register_dict = du.add_user_to_database(email, ah.hash_data(password),\
        name_first, name_last, ah.create_handle(name_first, name_last), \
        u_id_returned \
    )

    return register_dict 


def auth_login(email, password):
    # Validate Email
    ah.validate_email(email)
    user_rec =  dr.get_users_by_key("email", email)
    if user_rec == []:
        raise InputError(description='Email entered does not belong to a user')
    
    # Validate Password
    hash_pw = ah.hash_data(password)
    if hash_pw != user_rec[0]["password"]:
        raise InputError(description='Password is not correct')

    # Create and assign token to database
    # new_token = ah.get_valid_token(email)
    login_dict = du.login_user(email)

    return login_dict


def auth_logout(token):
    is_success = du.logout_user(token)
    return {"is_success": is_success}
