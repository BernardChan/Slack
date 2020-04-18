"""
 database_retrieval.py
This file contains functions to query the database, so to avoid directly accessing
database at all times possible since implementation/structure may change
during the agile iteration process.

# Usage:
#   Functions ending with "_by_key(key, value)"
#   - Accept a "key" and a "value"
#   - The key tells the function what part of the dictionary you want to check
#   - The value tells the function what to match
#       e.g. I want all users with the first name Hayden:
#       get_users_by_key("name_first", "Hayden")

# Additions
    # 21/03/20
    # added is_duplicate moved here from auth file.
"""

# pylint: disable=W0105 #pointless-string-statement
import database_files.database as db

"""
----------------------------------------------------------------------------------
Database Get Functions
----------------------------------------------------------------------------------
"""
def get_messages():
    """Returns messages list"""
    return db.DATABASE["messages"]

def get_channels():
    """Returns channels list"""
    return db.DATABASE["channels"]

def get_users():
    """Returns users list"""
    return db.DATABASE["users"]


def get_messages_by_key(key, value):
    """returns all messages of given key"""
    messages = get_messages()
    return_messages = []

    # Find what channels a user is in
    for message in messages:
        print("searching")
        if message[key] == value:
            print(f"message was {message}\n message_id was {value}\n\n")
            return_messages.append(message)

    print(f"returning messages: {return_messages}")
    return return_messages

def get_channel_messages(channel_id):
    """returns all messages from a given channel_id"""
    messages = db.DATABASE["messages"]
    return [message for message in messages if message["channel_id"] == channel_id]

def get_channels_by_key(key, value):
    """gets channels by key"""
    channels = get_channels()
    return [channel for channel in channels if channel[key] == value]

def get_channel_standup(channel_id):
    """gets the standup queue in channel_id"""
    channel = get_channels_by_key("channel_id", channel_id)[0]
    return channel["standup"]


"""
----------------------------------------------------------------------------------
Database Query Functions
----------------------------------------------------------------------------------
"""
def get_users_by_key(key, value):
    """gets specific users by key"""
    users = get_users()
    return [user for user in users if user[key] == value]


def is_duplicate(key, value):
    """checks if given key is duplicate to one in the database"""
    db_user = get_users_by_key(key, value)
    if db_user != []:
        return True
    return False


def is_user_in_channel(key, value, channel_id):
    """
    Returns boolean if a user is part of a channel
    User key is what property (key) of the user we're searching
    e.g. is_user_in_channel("token", token, 2) # Checks if a user is in channel
    2 by their token
    e.g. is_user_in_channel("u_id", 6, 3) # Check if user is in channel 3 by their
    u_id (u_id = 6 here)
    """
    channels = get_channels()
    print(f"matching value {value}")
    # Go through the list of channels and check only the ones matching channel_id
    for channel in channels:
        if channel["channel_id"] == channel_id:
            print(f"found channel {channel_id}")
            # Find the member with the matching key/value pair.
            for member in channel["members"]:
                print(f"members were {member[key]}")
                if member[key] == value:
                    print("returning true")
                    return True
    return False


def is_owner_in_channel(key, value, channel_id):
    """returns boolean if a user is owner of a channel"""
    channels = get_channels()

    # Go through the list of channels and check only the ones matching channel_id
    for channel in channels:
        if channel["channel_id"] == channel_id:

            # Find the member with the matching key/value pair.
            for member in channel["owner_members"]:
                if member[key] == value:
                    return True
    return False


def get_user_channels_by_key(key, value):
    """Gets all the channels a user is a part of"""
    channels = get_channels()

    user_channels = []

    # Find what channels a user is in
    for channel in channels:
        for user in channel["members"]:
            # If we found the user's token in one of the channels
            # Add it to user_channels
            if user[key] == value:
                user_channels.append(channel)

    return user_channels
