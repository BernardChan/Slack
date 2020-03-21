"""
 database.py
# This function stores input given from a file. Preserving the state by pickling the results and unpickling it when data needs to be added. All of the functions that directly access data are also added here. 

"""
# Usage
    
# Example of what the database will look like available in 
# If you have additions, add them, make a merge request, and post it on slack.
# Make sure all the keys are there when you're adding to this
# Additions:
# - "token" key added to "user" dictionary
# - "channel_id" key added to "message" dictionary
# - "members" key added to "channels" dictionary
# 21/03/20 Additions
    # - "permission_id added to user. 1 for owner and 2 for everyone else


import pickle
from os import path
import os
from database_files.database_retrieval import get_users


DATABASE = {
    "users": [],
    "messages": [],
    "channels": [],
}

unpickle = False

"""
----------------------------------------------------------------------------------
Core Database Functions
----------------------------------------------------------------------------------
"""    
# Saves the current database_files
def pickle_database():
    if path.exists("../database_files/database.p"):
        with open("../database_files/database.p", "wb") as FILE:
            pickle.dump(DATABASE, FILE)
    else:
        filename = "../database_files/database.p"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open("../database_files/database.p", "wb") as FILE:
            pickle.dump(DATABASE, FILE)
    unpickle = False

# Restores the database_files from last save
def unpickle_database():
    global DATABASE
    if path.exists("../database_files/database.p"):
        DATABASE = pickle.load(open("../database_files/database.p", "rb"))
    else:
        DATABASE = {
            "users": [],
            "messages": [],
            "channels": [],
        }
    unpickle = True
        
# Function to clear the database
def clear_database():
    global DATABASE
    DATABASE = {
    "users": [],
    "messages": [],
    "channels": [],
}  
    pickle_database()

"""
----------------------------------------------------------------------------------
Data Entry Functions
----------------------------------------------------------------------------------
"""    
# Adding user.
def add_user_to_database(email, password, name_first, name_last, handle, token, u_id):
    if not unpickle:
        unpickle_database()
    global DATABASE
    
    permission_id = 0
    #if u_id == 1:
    if len(get_users()) == 0:
        permission_id = 1
    else:
        permission_id = 2
    
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

    DATABASE['users'].append(new_user)
    pickle_database()
    
    
    
def login_user(email, token):
    if not unpickle:
        unpickle_database()
    global DATABASE
    i = 0
    for user in get_users():
        if user["email"] == email:
            existing_user = user
            #index = user['u_id'] - 1
            DATABASE['users'][i]['token'] = token
        i += 1
                    
    ret_u_id = existing_user['u_id']
    return {
        'u_id': ret_u_id,
        'token': token,
    }
    pickle_database()
    
"""
def logout_user(token):
    if not unpickle:
        unpickle_database()
    existing_user = get_users_by_key("token", token)
    existing_user['token'] = ""
    return True
    pickle_database()
"""


def logout_user(token):
    if not unpickle:
        unpickle_database()
    for user in get_users():
        if user["token"] == token:
            existing_user = user
    print(user)
    existing_user['token'] = token
    ret_u_id = existing_user['u_id']
    return {
        'u_id': ret_u_id,
        'token': token,
    }
    pickle_database()
    
    
unpickle_database
