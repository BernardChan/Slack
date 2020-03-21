"""
 database.py
# This function stores input given from a file. Preserving the state by pickling the results and unpickling it when data needs to be added. All of the functions that directly access data are also added here. 

"""
# Usage
    

import pickle
from os import path
import os


DATABASE = {
    "users": [],
    "messages": [],
    "channels": [],
}

DATABASE_EMPTY = {
    "users": [],
    "messages": [],
    "channels": [],
}

unpickle = False

# Example of what the database will look like.
# If you have additions, add them, make a merge request, and post it on slack.
# Make sure all the keys are there when you're adding to this
# Additions:
# - "token" key added to "user" dictionary
# - "channel_id" key added to "message" dictionary
# - "members" key added to "channels" dictionary
# 21/03/20 Additions
    # - "permission_id added to user. 1 for owner and 2 for everyone else

# Returns messages list
def get_messages():
    global DATABASE
    return DATABASE["messages"]

# Returns channels list
def get_channels():
    global DATABASE
    return DATABASE["channels"]

# Returns users list
def get_users():
    global DATABASE
    return DATABASE["users"]
    



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
    global DATABASE_EMPTY
    DATABASE = DATABASE_EMPTY
    pickle_database()

# Adding user.
def add_user_to_database(email, password, name_first, name_last, handle, token, u_id):
    if not unpickle:
        unpickle_database()
    global DATABASE
    #print("Initial Database Printout VVVVVVVVVVVVVVVVVVVVVV")
    #print(DATABASE)
    #print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    permission_id = 0
    if u_id == 1:
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
    print("Database Printout VVVVVVVVVVVVVVVVVVVVVV")
    print(DATABASE)
    print("^^^^^^^^^^^^^^^^^^^^^^^^")
    pickle_database()
    
    
    
def login_user(email, token):
    #print("These are the arguments passed into login_user")
    #print(f"Email = {email}")
    #rint(f"Token = {token}")
    if not unpickle:
        unpickle_database()
    global DATABASE
    i = 0
    for user in get_users():
        #print(f"Pass {i} ==========================")
        #print(f"User[{i}] = {user['email']}")
        #print(f"Email   = {email}") 
        if user["email"] == email:
            print("True")
            existing_user = user
            #user['token'] = token
            index = user['u_id'] - 1
            print(f"Index{index}")
            print(f"Before: {DATABASE['users'][index]['token']}")
            DATABASE['users'][index]['token'] = token
            print(f"After: {DATABASE['users'][index]['token']}")
            
            #j = i
            print(f"Existing user = {existing_user['email']}")
        i += 1
        
    #print("this is the user selected by the database.login_user() function")
    #print(existing_user["email"])
    # existing_user['token'] = token
    #print(f"DATABASE token b4 = {DATABASE['users'][j]['token']}")
    #DATABASE['users'][j]['token'] = token
    #print(f"DATABASE token aft = {DATABASE['users'][j]['token']}")
    
    ret_u_id = existing_user['u_id']
    # ret_u_id = DATABASE['users'][j]['u_id']
    #print(f"ret_u_id = {ret_u_id}")
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
