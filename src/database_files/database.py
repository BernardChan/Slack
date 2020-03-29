"""
 database.py
# This function stores database files. Preserving the state by pickling the results and unpickling it when data needs to be added. 

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
# from database_files.database_retrieval import get_users


DATABASE = {
    "users": [],
    "messages": [],
    "channels": [],
}

# unpickle = False

"""
----------------------------------------------------------------------------------
Core Database Functions
----------------------------------------------------------------------------------
"""    
# # Saves the current database_files
# def pickle_database(): 
#     global DATABASE
#     with open("../database_files/database.p", "wb") as FILE:
#         pickle.dump(DATABASE, FILE)


# # Restores the database_files from last save
# def unpickle_database():
#     global DATABASE
#     if path.exists("../database_files/database.p"):
#         DATABASE = pickle.load(open("../database_files/database.p", "rb"))
#     else:
#         DATABASE = {
#             "users": [],
#             "messages": [],
#             "channels": [],
#         }
    

# Function to clear the database
def clear_database():
    global DATABASE
    DATABASE = {
    "users": [],
    "messages": [],
    "channels": [],
}
