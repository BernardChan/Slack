"""
File for functions that retrieve information from the Slackr database
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

# pylint: disable=W0105 #pointless-string-statement
import database_files.database as db

"""
----------------------------------------------------------------------------------
Database Get Functions
----------------------------------------------------------------------------------
"""
def get_messages():
    """
    Returns messages list
    :return: returns the database part containing all the messages
    """
    return db.DATABASE["messages"]

def get_channels():
    """
    Returns channels list
    :return: returns the database part containing all the channels
    """
    return db.DATABASE["channels"]

def get_users():
    """
    Returns users list
    :return: returns the database part containing all the users
    """
    return db.DATABASE["users"]


def get_messages_by_key(key, value):
    """
    Returns all messages of given key
    :param key: the key segment of the dictionary
    :param value: the value segment of the dictionary
    :return: returns a list containing all the messages that match the search
    """
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
    """
    Returns all messages from a given channel_id
    :param channel_id: the channel_id that will be used for the search
    :return: returns a list containing all the messages that match the channel_id
    """
    messages = db.DATABASE["messages"]
    return [message for message in messages if message["channel_id"] == channel_id]

def get_channels_by_key(key, value):
    """
    Returns channels that match a particular key and value
    :param key: the key segment of the search
    :param value: the value segment of the search
    :return: returns a list containing all the channels that match the search
    """
    channels = get_channels()
    return [channel for channel in channels if channel[key] == value]

def get_channel_standup(channel_id):
    """
    gets the standup queue in channel_id
    :param channel_id: the channel_id that will be used for the search
    :return: returns a list containing the queue in the standup channel
    """
    channel = get_channels_by_key("channel_id", channel_id)[0]
    return channel["standup"]


"""
----------------------------------------------------------------------------------
Database Query Functions
----------------------------------------------------------------------------------
"""
def get_users_by_key(key, value):
    """
    gets specific user by key
    :param key: the key segment of the search
    :param value: the value segment of the search
    :return: returns a list containing the user if one matched the search
    """
    users = get_users()
    return [user for user in users if user[key] == value]


def is_duplicate(key, value):
    """
    checks if given key/value is duplicate to one in the database and returns a boolean
    :param key: the key segment of the search
    :param value: the value segment of the search
    :return: returns a boolean of True or False
    """
    db_user = get_users_by_key(key, value)
    if db_user != []:
        return True
    return False


def is_user_in_channel(key, value, channel_id):
    """
    checks if given user is in a channel and returns a boolean if they are
    :param key: User key is what property (key) of the user being searched
    :param value: the value of the propery being searched
    :param channel_id: the id of the channel being searched
    :return: returns a boolean of True or False
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
    """
    checks if given user owns a channel and returns a boolean True if they are
    :param key: User key is what property (key) of the user being searched
    :param value: the value of the user propery being searched
    :param channel_id: the id of the channel being searched
    :return: returns a boolean of True or False
    """
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
    """
    Gets all the channels a user is a part of
    :param key: User key is what property (key) of the user being searched
    :param value: the value of the user propery being searched
    :return: returns a list of channels mathcing search criteria
    """
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
