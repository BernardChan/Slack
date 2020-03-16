# Example DATABASE shown at the bottom of the file
# Gives 2 functions to save and restore the DATABASE from database_files.py

import pickle

DATABASE = {
    "users": [],
    "messages": [],
    "channels": [],
}

# Example of what the database will look like.
# If you have additions, add them, make a merge request, and post it on slack.
# Make sure all the keys are there when you're adding to this
# Additions:
# - "token" key added to "user" dictionary
# - "channel_id" key added to "message" dictionary
# - "members" key added to "channels" dictionary
MOCK_DATA = {
    "users": [
        {"u_id": 0, "email": "asd@asd.com", "name_first": "0", "name_last": "0", "handle_str": "0", "token": 0},
        {"u_id": 1, "email": "asd1@asd.com", "name_first": "1", "name_last": "1", "handle_str": "1", "token": 1},
        {"u_id": 2, "email": "asd2@asd.com", "name_first": "2", "name_last": "2", "handle_str": "2", "token": 2}
    ],

    "messages": [
        {
            "message_id": 0,
            "u_id": 0,
            "message": "str",
            "time_created": 0,
            "reacts": {"react_id": 0, "u_ids": [0, 1, 2], "is_this_user_reacted": False},
            "is_pinned": False,
            "channel_id": 0,
        },
        {
            "message_id": 1,
            "u_id": 1,
            "message": "1str",
            "time_created": 1,
            "reacts": {"react_id": 1, "u_ids": [0, 1, 2], "is_this_user_reacted": False},
            "is_pinned": False,
            "channel_id": 1},

        {
            "message_id": 2,
            "u_id": 2,
            "message": "2str",
            "time_created": 2,
            "reacts": {"react_id": 1, "u_ids": [0, 1, 2], "is_this_user_reacted": False},
            "is_pinned": False,
            "channel_id": 2
        }
    ],

    "channels": [
        {
            "channel_id": 0,
            "name": "0",
            "members": [{"u_id": 0, "name_first": "0", "name_last": "0", "token": 0}]
        },
        {
            "channel_id": 1,
            "name": "1",
            "members": [{"u_id": 1, "name_first": "1", "name_last": "1", "token": 1}]

        },

        {
            "channel_id": 2,
            "name": "2",
            "members": [{"u_id": 2, "name_first": "2", "name_last": "2", "token": 2}]
        }
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
