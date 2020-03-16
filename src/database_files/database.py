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

MOCK_DATA = {
    "users": [
        {"u_id": 0, "email": "asd@asd.com", "name_first": "0", "name_last": "0", "handle_str": "0", "token": 0},
        {"u_id": 1, "email": "asd1@asd.com", "name_first": "1", "name_last": "1", "handle_str": "1"},
        {"u_id": 2, "email": "asd2@asd.com", "name_first": "2", "name_last": "2", "handle_str": "2"}
    ],

    "messages": [
        {"message_id": 0, "u_id": 0, "message": "str", "time_created": 0,
            "reacts": {"react_id": 0, "u_ids": [0, 1, 2], "is_this_user_reacted": False},
         "is_pinned": False, "channel_id": 0},
        {"message_id": 1, "u_id": 1, "message": "1str", "time_created": 1, "reacts": None, "is_pinned": False, "channel_id": 1},
        {"message_id": 2, "u_id": 2, "message": "2str", "time_created": 2, "reacts": None, "is_pinned": False, "channel_id": 2}
    ],

    "channels": [
        {"channel_id": 0, "name": "0", "members": [{"u_id": 0, "name_first": "0", "name_last": "0"}]},
        {"channel_id": 1, "name": "1"},
        {"channel_id": 2, "name": "2"}
    ],
}


# Saves the current database_files
def pickle_database():
    with open("database.p", "wb") as FILE:
        pickle.dump(DATABASE, FILE)


# Restores the database_files from last save
def unpickle_database():
    global DATABASE
    DATABASE = pickle.load(open("database.p", "rb"))


unpickle_database()
