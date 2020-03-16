# File for functions to interface with the database
# Avoid directly accessing database since implementation/structure may change (A G I L E LUL)
# Basically lets us work on our functions without
#   having to wait for everyone to agree on a database structure

import database_files.database as db


def get_messages():
    return db.DATABASE["messages"]


# Returns all channel dictionaries
def get_channels():
    return db.DATABASE["channels"]


def get_users():
    return db.DATABASE["users"]


# returns all messages from a given channel_id
def get_channel_messages(channel_id):
    messages = db.DATABASE["messages"]
    # messages = db.MOCK_DATA["messages"]

    return [message for message in messages if message["channel_id"] == channel_id]


# Gets all the channels a user is a part of
def get_user_channels(token):
    channels = get_channels()

    user_channels = []

    # Find what channels a user is in
    for channel in channels():
        for user in channel["members"]:

            # If we found the user's token in one of the channels
            # Add it to user_channels
            if token == user["token"]:
                user_channels.append(channel["channel_id"])

    return user_channels


if __name__ == "__main__":
    print(get_channel_messages(0))
