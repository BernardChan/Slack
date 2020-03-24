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
# - "permission_id" key added to "user" dictionary (1 = owner/admin, 2 = member)
# - "members" key added to "channels" dictionary
# - "standup" key added to "channels" dictionary - is a boolean for whether a standup is active
# - "is_public" key to "channels" dictionary - boolean for whether the channel is public or not
# - "owner_members" key to "channels" dictionary - list of {user} who are owners of the channel. They will be repeated
#   in the "members" dictionary as well
MOCK_DATA = {
    "users": [
        {"u_id": 0, "email": "asd@asd.com", "name_first": "first0", "name_last": "last0", "handle_str": "handle0", "token": "0", "permission_id": 1},
        {"u_id": 1, "email": "asd1@asd.com", "name_first": "first1", "name_last": "last1", "handle_str": "handle1", "token": "1", "permission_id": 2},
        {"u_id": 2, "email": "asd2@asd.com", "name_first": "first2", "name_last": "last2", "handle_str": "handle2", "token": "2", "permission_id": 2}
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
            "owner_members": [{"u_id": 0, "name_first": "first0", "name_last": "last0", "token": 0}],
            "members": [{"u_id": 0, "name_first": "first0", "name_last": "last0", "token": 0}],
            "standup": {"active": False, "msg_queue": "", "time_finish": None},
            "is_public": False
        },
        {
            "channel_id": 1,
            "name": "1",
            "owner_members": [{"u_id": 0, "name_first": "first0", "name_last": "last0", "token": 0}],
            "members": [{"u_id": 1, "name_first": "first1", "name_last": "last1", "token": 1},
                        {"u_id": 0, "name_first": "first0", "name_last": "last0", "token": 0}],
            "standup": {"active": False, "msg_queue": "", "time_finish": None},
            "is_public": False
        },

        {
            "channel_id": 2,
            "name": "2",
            "owner_members": [{"u_id": 2, "name_first": "first2", "name_last": "last2", "token": 2}],
            "members": [{"u_id": 2, "name_first": "first2", "name_last": "last2", "token": 2}],
            "standup": {"active": False, "msg_queue": "", "time_finish": None},
            "is_public": False
        }
    ],
}


# Saves the current database_files
def pickle_database():
    with open("database_files/database.p", "wb") as FILE:
        pickle.dump(MOCK_DATA, FILE)


# Restores the database_files from last save
def unpickle_database():
    global DATABASE
    DATABASE = pickle.load(open("database_files/database.p", "rb"))


pickle_database()
unpickle_database()
