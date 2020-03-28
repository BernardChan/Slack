"""
 database_update.py
This file contains functions to change or add data to the database, so to avoid directly accessing database at all times possible since implementation/structure may change during the agile iteration process.
"""

import database_files.database as db
from helper_functions.auth_helper import hash_data
from datetime import datetime

"""
----------------------------------------------------------------------------------
Token Functions
----------------------------------------------------------------------------------
""" 
def get_valid_token(email):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    unique_combo = current_time + email
    token = hash_data(unique_combo)
    return token


"""
----------------------------------------------------------------------------------
Data Entry Functions
----------------------------------------------------------------------------------
"""    
# Adding user.
def add_user_to_database(email, password, name_first, name_last, handle, u_id):
    #db.unpickle_database()
    #global DATABASE
    
    permission_id = 0
    #if u_id == 1:
    if len(db.DATABASE["users"]) == 0:
        permission_id = 1
    else:
        permission_id = 2
    
    token = get_valid_token(email)
    
    new_user = {
        "u_id": u_id, 
        "email": email, 
        "password": password,
        "name_first": name_first, 
        "name_last": name_last, 
        "handle_str": handle, 
        "token": token,
        "permission_id": permission_id
    }

    db.DATABASE['users'].append(new_user)
    print(db.DATABASE['users'])
    #db.pickle_database()
    
    register_dict = {
        'u_id' : u_id,
        'token' : token
    }
    return register_dict
    
    
def login_user(email):
    #db.unpickle_database()
    #global DATABASE
    
    for user in db.DATABASE['users']:
        if user["email"] == email:
            token = get_valid_token(email)
            db.DATABASE['users'][user['u_id'] - 1]['token'] = token
            u_id = user['u_id']

    #db.pickle_database()
    return {
        'u_id': u_id,
        'token': token,
    }
    
    
def logout_user(token):
    #db.unpickle_database()
    #global DATABASE

    is_success = False
    for user in db.DATABASE['users']:
        if user["token"] == token:
            db.DATABASE['users'][user['u_id'] - 1]['token'] = ""
            is_success = True
    #db.pickle_database()
    return is_success
