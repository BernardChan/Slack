# Example DATABASE shown at the bottom of the file
# Gives 2 functions to save and restore the DATABASE from database_files.py

# TODO: determine file structure
'''
    Ideas:
    - Have users, messages, channels all separated, with
    users/messages having a key to denote what channel they're from/a part of
        Advantages: Don't have to repeat storage of a list of users for a particular channel
        Disadvantages: O(n) retrieval of users/messages of a particular channel

    - Have users/messages be a key for each channel
        "channels": {"messages": [], "users": []}
        Advantages: O(1) to get messages/users for a particular channel
        Disadvantages: can have repeated storage of the same thing
            e.g. a user will be stored in channel1 and in channel2, instead of once in "users":[]

'''

import pickle

DATABASE = {
    "users": [],
    "messages": [],
    "channels": [],
}


# Saves the current database_files
def pickle_database():
    with open("database_files.p", "wb") as FILE:
        pickle.dump(DATABASE, FILE)


# Restores the database_files from last save
def unpickle_database():
    global DATABASE
    DATABASE = pickle.load(open("database_files.p", "rb"))


unpickle_database()
