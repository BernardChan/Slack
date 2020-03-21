"""
 auth.py
# This function takes in input from the user, validates it, checks against the database, then authenticates them if everything is correct.

"""
from error import AccessError, InputError
from database_files.database import get_users
from database_files.database_retrieval import get_users_by_key
# import database_files.database as db
from database_files.database import add_user_to_database
from database_files.database import clear_database
from database_files.database import login_user
from database_files.database import logout_user

import pytest
import hashlib
from datetime import datetime
import re

"""
----------------------------------------------------------------------------------
Validation Functions
----------------------------------------------------------------------------------
"""
def validate_email(email):
    regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if(re.search(regex,email)): 
        return True
    else:  
        raise InputError(description='Incorrect email format')
        return False
               
        
def validate_password(password):
    if len(password) >= 6: 
        return True
    else:  
        raise InputError(description='Password must be 6 or more characters long')
        return False


def validate_name_first(name_first):
    # name_first not is between 1 and 50 characters inclusive in length
    if len(name_first) >= 1 and len(name_first) <= 50:
        return True
    else:
        raise InputError(description = 'First name must be 1 to 50 characters long') 
        return False  
        
        
def validate_name_last(name_last):
    # name_last is not between 1 and 50 characters inclusive in length
    if len(name_last) >= 1 and len(name_last) <= 50:
        return True
    else:
        raise InputError(description = 'Last name must be 1 to 50 characters long')
        return False

"""
----------------------------------------------------------------------------------
Database Checking Functions
----------------------------------------------------------------------------------
"""        
def duplicate_check(key, value):
    db_user = get_users_by_key(key, value)
    #print(f"Database Duplicate = {db_user}")
    if db_user != []:
        return True
    else:
        return False 


def get_u_id():
    u_id_last = len(get_users()) + 1
    #print(f"Get u_id length = {len(get_users())}")
    #print(get_users())
    return u_id_last
    

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
    return {
        'is_success': True,
    }


def auth_register(email, password, name_first, name_last):
    # Stage 1 - Validate input. 
    validate_email(email)
    validate_password(password)
    validate_name_first(name_first)
    validate_name_last(name_last)
    
    # Stage 2 - Generate input transformations
    hashed_password = hash_data(password)
    token = get_valid_token(email)
    
    # Stage 3 - check database
    if duplicate_check("email", email):
        raise InputError(description = 'Email address is already being used by another user')
    u_id_returned = get_u_id()
    handle = create_handle(name_first, name_last)
    
    # Stage 4 - Store all user information in the database
    add_user_to_database(email, \
        hashed_password, name_first, name_last, \
        handle, token, u_id_returned \
    )
    register_dict = {}
    register_dict['u_id'] = u_id_returned
    register_dict['token'] = token
    return register_dict
