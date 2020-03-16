from error import InputError, AccessError
import database_files.database_retrieval as db


# Check is a channel_id is valid
# Returns true if it finds the channel with channel_id, else false
def channel_is_valid(channel_id):
    return True if db.get_channels_by_key("channel_id", channel_id) else False


# Throw InputError when number of chars > 1000
# Accepts a string for a message
def check_message_length(message):
    if len(message) > 1000:
        raise InputError("Message exceeded 1000 Characters")


# Check if a channel is valid (if the channel exists)
def check_channel_validity(channel_id):
    if not channel_is_valid(channel_id):
        raise InputError("The given channel_id was not found")


# check if a token is part of a channel with channel_id
def check_member_status_of_channel(token, channel_id):
    if not db.is_user_in_channel("token", token, channel_id):
        raise AccessError("Invalid channel_id provided")


# Throws errors where needed
def is_message_valid(token, message, channel_id):
    check_message_length(message)

    check_channel_validity(channel_id)

    check_member_status_of_channel(token, channel_id)
