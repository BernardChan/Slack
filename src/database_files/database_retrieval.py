"""
 database_retrieval.py
This file contains functions to query the database, so to avoid directly accessing database at all times possible since implementation/structure may change during the agile iteration process.
"""

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

# import database_files.database as db
import database_files.database as db

"""
----------------------------------------------------------------------------------
Database Get Functions
----------------------------------------------------------------------------------
"""
# Returns messages list
def get_messages():
    return db.DATABASE["messages"]

# Returns channels list
def get_channels():
    return db.DATABASE["channels"]

# Returns users list
def get_users():
    return db.DATABASE["users"]
    
# returns all messages from a given channel_id
def get_channel_messages(channel_id):
    messages = db.DATABASE["messages"]
    return [message for message in messages if message["channel_id"] == channel_id]
    
# gets channels by key
def get_channels_by_key(key, value):
    channels = get_channels()
    return [channel for channel in channels if channel[key] == value]
    
# gets the standup queue in channel_id
def get_channel_standup(channel_id):
    channel = get_channels_by_key("channel_id", channel_id)[0]
    return channel["standup"]


"""
----------------------------------------------------------------------------------
Database Query Functions
----------------------------------------------------------------------------------
"""    

# gets specific users by key
def get_users_by_key(key, value):
    users = get_users()
    return [user for user in users if user[key] == value]
    
    
def is_duplicate(key, value):
    db_user = get_users_by_key(key, value)
    if db_user != []:
        return True
    else:
        return False 


# returns boolean if a user is part of a channel
# user key is what property (key) of the user we're searching
# e.g. is_user_in_channel("token", token, 2) # Checks if a user is in channel 2 by their token
# e.g. is_user_in_channel("u_id", 6, 3) # Check if a user is in channel 3 by their u_id (u_id = 6 here)
def is_user_in_channel(key, value, channel_id):
    channels = get_channels()

    # Go through the list of channels and check only the ones matching channel_id
    for channel in channels:
        if channel["channel_id"] == channel_id:

            # Find the member with the matching key/value pair.
            for member in channel["members"]:
                if member[key] == value:
                    return True
    return False


# returns boolean if a user is owner of a channel
def is_owner_in_channel(key, value, channel_id):
    channels = get_channels()

    # Go through the list of channels and check only the ones matching channel_id
    for channel in channels:
        if channel["channel_id"] == channel_id:

            # Find the member with the matching key/value pair.
            for member in channel["owner_members"]:
                if member[key] == value:
                    return True
    return False



# Gets all the channels a user is a part of
def get_user_channels_by_key(key, value):
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

if __name__ == "__main__":
    pass
