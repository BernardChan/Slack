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
Input Transformation Functions
----------------------------------------------------------------------------------
"""
def hash_data(data):
    hashed_data = hashlib.sha256(data.encode()).hexdigest()
    return hashed_data
    
    
    
def get_valid_token(email):
    #current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    # print("Something weird is happening with tokens")
    # print(f"Current Time {current_time}")
    # print(f"Direct time {datetime.now()}")
    unique_combo = current_time + email
    # print(f"unique_combo = {unique_combo}")
    token = hash_data(unique_combo)
    # print(token)
    return token
    
    

def create_handle(name_first, name_last):
    handle = name_first + "." + name_last
    handle = handle.lower()
    #print(handle)
    #shave down length if needed
    if len(handle) > 20:
        handle = handle[0:20]
        #print(handle)
    # Add hashed digits until unique
    #stored = get_users_by_key("handle_str", handle)
    while duplicate_check("handle_str", handle):
        hashed_input = hash_data(handle).upper()
        character = handle[0:-1] + hashed_input[1]
        handle = character
        #print(handle)
        # stored = get_users_by_key("handle_str", handle)
    #print(handle)
    return handle
    
    
"""
----------------------------------------------------------------------------------
User Interface Functions
----------------------------------------------------------------------------------
"""     
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
    # ASSUMPTION If the user IS registered then I will fail the registration attempt.
    if duplicate_check("email", email):
        raise InputError(description = 'Email address is already being used by another user')
    u_id_returned = get_u_id()
    handle = create_handle(name_first, name_last)
    
    # Stage 4 - Store all user information in the database
    add_user_to_database(email, \
        hashed_password, name_first, name_last, \
        handle, token, u_id_returned \
    )
    # permission_id complete
    
    register_dict = {}
    register_dict['u_id'] = u_id_returned
    register_dict['token'] = token
    return register_dict
     
 
        
def auth_login(email, password):
    # Validate email
    validate_email(email)
    
    # TODO Search by email, find record.
    user_rec = get_users_by_key("email", email)
    #print(user_rec)
    #print("Step 1")
    #print("This is user Record Selected")
    #print(user_rec[0])
    if user_rec == []:
        raise InputError(description = 'Email entered does not belong to a user')
    
    # Hash password, see if it matches.
    hash_pw = hash_data(password)
    #print("Step 2")
    #print(f"pass stored = {user_rec[0]['password']}")
    #print(f"pass   new  = {hash_pw}")
    if hash_pw != user_rec[0]["password"]:
        raise InputError(description = 'Password is not correct')
    #else:
        #print("Step 3")
        #print("Yee boi dat shit match")
    
    new_token = get_valid_token(email)
    login_dict = login_user(email, new_token)
    # TODO resolve strange behavior here
    
    # Return dict of u_id and token
    #print("This is the login_dict that is returning")
    #print(login_dict)
    return login_dict
        
        
        
def auth_logout(token):
    # TODO Search user by token
    user_rec = get_users_by_key("token", token)
    if user_rec == []:
        return {
        'is_success': False,
    }
    else:
        logout_user(token)
        # TODO Remove Token
        # TODO Return true on succcessful logout
    return {
        'is_success': True,
    }

    
if __name__ == '__main__':
    clear_database()
    item1 = auth_register("dankoenen0@gmail.com", "password@123", "Daniel", "Koenen")
    print("Register 1")
    print(f"Item 1 = {item1['u_id']} : {item1['token']}")
    print("=================================")
    
    item2 = auth_register("cutiepie@gmail.com", "password@123", "Daniellellaqueze", "Koenenopolis")
    print("Register 2")
    print(f"Item 2 = {item2['u_id']} : {item2['token']}")
    print("=================================")
    
    item3 = auth_register("cutiepie1@gmail.com", "password@123", "AlphaBetaCharlie", "DeltaEchoFoxtrot")
    print("Register 3")
    print(f"Item 3 = {item3['u_id']} : {item3['token']}")
    print("=================================")
    
    
    print("=================================")
    print("=================================")
    print("=================================")
    print("=================================")
    #Shoud fail because the email matches. 
    #item4 = auth_register("dankoenen0@gmail.com", "password@123", "Daniel", "Koenen")
    #print(f"Item 4 = {item4['u_id']} : {item4['token']}")
    
    print("Login 1")
    login1 = auth_login("dankoenen0@gmail.com", "password@123")
    print(f"Login1 = {login1['u_id']} : {login1['token']}")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("Login 2")
    login2 = auth_login("cutiepie1@gmail.com", "password@123")
    print(f"login2 = {login2['u_id']} : {login2['token']}")
    
    print("=================================")
    
    item4 = auth_register("yomumma@gmail.com", "eyylmaoboi", "Waddup", "MyLadski")
    print("Register 4")
    print(f"Item 4 = {item4['u_id']} : {item4['token']}")
    
    #auth_logout("dankoenen0@gmail.com")
