from error import InputError, AccessError
import database_files.database_retrieval as db
from database_files.database import DATABASE
import uuid


# Check is a channel_id is valid
# Returns true if it finds the channel with channel_id, else false
def channel_is_valid(channel_id):

    array = db.get_channels_by_key("channel_id", channel_id)
    return True if array else False


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
        raise AccessError("User was not a member of the channel_id provided")


# Throws errors where needed
def is_message_valid(token, message, channel_id):
    check_message_length(message)

    check_channel_validity(channel_id)

    check_member_status_of_channel(token, channel_id)


def is_user_valid_channel_member(token, channel_id):
    if not db.is_user_in_channel("token", token, channel_id):
        raise AccessError(f"User is not in channel with channel_id {channel_id}")


# Checks if u_id actually exists for a profile, throws Inputerror if not
def is_valid_uid(u_id):
    if db.get_users_by_key("u_id", u_id) == []:
        raise InputError(description="The given user id was not found!")


# Checks whether a user with token is an admin or owner, throws Accesserror if not
def is_slackr_admin(token):
    match = db.get_users_by_key("token", token)
    if (match[0]["permission_id"] != 1):
        raise AccessError(description="User is not an admin or owner!")

def is_valid_token(token):
    if db.get_users_by_key("token", token) == []:
        raise AccessError(description="The given token was not found!")


# Returns a unique 15 digit long integer
def get_unique_id():
    # bit shifting it so the number is smaller and doesn't reveal mac address
    return int(uuid.uuid1())>>80  