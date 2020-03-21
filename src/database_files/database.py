# Example DATABASE shown at the bottom of the file
# Gives 2 functions to save and restore the DATABASE from database_files.py

import pickle

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
# Additions:
# - "token" key added to "user" dictionary
# - "channel_id" key added to "message" dictionary
# - "members" key added to "channels" dictionary
# 21/03/20 Additions
    # - "permission_id added to user. 1 for owner and 2 for everyone else


"""
----------------------------------------------------------------------------------
Query Functions
----------------------------------------------------------------------------------
""" 
# These functions full information from the database.

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
    

"""
----------------------------------------------------------------------------------
Database Functions
----------------------------------------------------------------------------------
""" 
# These functions support the large scale operation of the database.

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
    
"""
----------------------------------------------------------------------------------
Data Operation Functions
----------------------------------------------------------------------------------
""" 
# These functions actually change data in the database.
    
# Adding user.
def add_user_to_database(email, password, name_first, name_last, handle, token, u_id):
    if not unpickle:
        unpickle_database()
    global DATABASE
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
    pickle_database()


# pickle_database()
unpickle_database()
