"""
 database.py
# This function stores input given from a file. Preserving the state by pickling the results and unpickling it when data needs to be added. All of the functions that directly access data are also added here. 

"""
# Usage

# Example of what the database will look like:
# Available in database_plan.md
# If you have additions, add them, make a merge request, and post it on slack.
# Make sure all the keys are there when you're adding to this

# Additions:
# - "token" key added to "user" dictionary
# - "channel_id" key added to "message" dictionary
# - "members" key added to "channels" dictionary
# - "standup" key added to "channels" dictionary - is a boolean for whether a standup is active
# 21/03/20 Additions
    # - "permission_id added to user. 1 for owner and 2 for everyone else
# 23/03/20 Additions
    # Login and logout working


import pickle
from os import path
import os
from database_files.database_retrieval import get_users


DATABASE = {
    "users": [],
    "messages": [],
    "channels": [],
}


"""
----------------------------------------------------------------------------------
Core Database Functions
----------------------------------------------------------------------------------
"""    
# Saves the current database_files
def pickle_database(): 
    global DATABASE
    with open("../database_files/database.p", "wb") as FILE:
        pickle.dump(DATABASE, FILE)


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
   
    unpickle_database() # delete
    global DATABASE

    permission_id = 0
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
    unpickle_database() # delete
    global DATABASE

    for user in get_users():
        if user["email"] == email:
            DATABASE['users'][user['u_id'] - 1]['token'] = token
            u_id = user['u_id']

    pickle_database()
    return {
        'u_id': u_id,
        'token': token,
    }
    
    
def logout_user(token):
    unpickle_database() # delete
    global DATABASE

    is_success = False
    for user in get_users():
        if user["token"] == token:
            DATABASE['users'][user['u_id'] - 1]['token'] = ""
            is_success = True
    pickle_database()
    return is_success
    
unpickle_database
