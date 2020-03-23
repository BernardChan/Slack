from error import AccessError, InputError

import pytest
import hashlib
from datetime import datetime
import re

import database_files.database_retrieval as dr

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
        
        
def validate_password(password):
    if len(password) >= 6: 
        return True
    else:  
        raise InputError(description='Password must be 6 or more characters long')


def validate_name_first(name_first):
    # name_first not is between 1 and 50 characters inclusive in length
    if len(name_first) >= 1 and len(name_first) <= 50:
        return True
    else:
        raise InputError(description = 'First name must be 1 to 50 characters long') 
        
        
def validate_name_last(name_last):
    # name_last is not between 1 and 50 characters inclusive in length
    if len(name_last) >= 1 and len(name_last) <= 50:
        return True
    else:
        raise InputError(description = 'Last name must be 1 to 50 characters long')
        
        
"""
----------------------------------------------------------------------------------
Input Transformation Functions
----------------------------------------------------------------------------------
"""
def hash_data(data):
    hashed_data = hashlib.sha256(data.encode()).hexdigest()
    return hashed_data
    
    
def get_valid_token(email):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    unique_combo = current_time + email
    token = hash_data(unique_combo)
    return token
    

def create_handle(name_first, name_last):
    handle = name_first + "." + name_last
    handle = handle.lower()
    if len(handle) > 20:
        handle = handle[0:20]
    while dr.duplicate_check("handle_str", handle):
        hashed_input = hash_data(handle).lower()
        character = handle[0:-1] + hashed_input[1]
        handle = character
    return handle
    
 
def get_u_id():
    u_id_last = len(database.get_users())
    while dr.duplicate_check("u_id", u_id_last):
        u_id_last += 1
    # u_id_last = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return u_id_last

