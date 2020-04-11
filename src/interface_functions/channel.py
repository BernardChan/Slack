# pylint: disable=W0105, W0622, C0200
import database_files.database_retrieval as db
from database_files.database import DATABASE
import helper_functions.interface_function_helpers as help
from error import InputError, AccessError


"""
File for functions relating to a Slackr channel
"""


def channel_invite(token, channel_id, u_id):
    return "Not Implemented"


# This needs to be fixed. members=DATABASE etc. doesn't work.
# Assigning the database to members does nothing. It isn't editing the database
# This needs to be fixed
def WIP_channel_invite(token, channel_id, u_id):
    # include valid token function here, stub function atm
    help.is_valid_token(token)

    # check if channel is valid
    help.check_channel_validity(channel_id)
    # check if user is a member of the channel
    help.is_user_valid_channel_member(token, channel_id)

    # check if user is valid
    help.is_valid_uid(u_id)

    # finds the user dictionary with user id and assigns it to user_invite
    for user in DATABASE["users"]:
        if user["u_id"] == u_id:
            user_invite = user

    # adds user to members list in channel
    members = DATABASE['channels'][channel_id]['members']
    members.append(dict(user_invite))

    return {
    }


# Given a Channel with ID channel_id that the authorised user is part of,
# provide basic details about the channel
def channel_details(token, channel_id):
    """
    Given a Channel with ID channel_id that the authorised user is part of,
    provide basic details about the channel
    :param token: authorised user's identifier
    :param channel_id: Integer for a specific channel
    :return: returns a dictionary with the channel name, owners, and members
    """
    help.is_valid_token(token)
    help.check_channel_validity(channel_id)
    help.check_member_status_of_channel(token, channel_id)

    channel = db.get_channels_by_key("channel_id", channel_id)[0]

    return {
        "name": channel["name"],
        "owner_members": channel["owner_members"],
        "all_members": channel["members"]
    }


# Finish is the ending index for the list slice, whereas
# end is the ending NUMBER to be returned by messages
# can't use -1 for slice notation since that return (n-1)th place
def get_finish_and_end(start, messages):
    """
    Get the starting and ending index of the given messages and start index
    :param start: integer for the first message
    :param messages: list of messages
    :return: returns a valid index range for the given list of messages
    """
    end = start + 50
    finish = end
    num_messages = len(messages)
    if start > num_messages:
        raise InputError("Start given was greater than the number of messages in the channel")

    # set finish to -1 if we don't have 50 messages to send back
    if num_messages < end:

        end = -1

    if end == -1:
        finish = len(messages)

    return finish, end


def channel_messages(token, channel_id, start):
    """
    Returns a list of messages that have been paginated for 50 messages
    :param token: authorised user's identifier
    :param channel_id: Integer for a specific channel
    :param start: integer for the starting index of a list of messages
    :return: returns the messages within the start and end indices
    """
    help.is_valid_token(token)
    # Check Errors
    help.check_channel_validity(channel_id)

    help.is_user_valid_channel_member(token, channel_id)

    messages = db.get_channel_messages(channel_id)

    # Get the finish index for messages and end index for return value
    finish, end = get_finish_and_end(start, messages)

    return {
        "messages": messages[start: finish],
        "start": start,
        "end": end,
    }

def channel_leave(token, channel_id):
    return "Not Implemented"


# TODO: Has problems similar to channel_join and leave
def WIP_channel_leave(token, channel_id):
    # include valid token function here, stub function atm
    help.is_valid_token(token)

    # check if channel is valid
    help.check_channel_validity(channel_id)

    # check if user is a member of the channel
    help.is_user_valid_channel_member(token, channel_id)

    # remove the authorised user from the channel
    mem = DATABASE['channels'][channel_id]['members']
    for i in range(len(mem)):
        if mem[i]['token'] == token:
            del mem[i]
            break

    return {
    }


def channel_join(token, channel_id):
    return "Not Implemented"


# TODO: Throws access error when the user is not the slackr owner, but the
# channel is public. Non-admins should be able to join public channels.
def WIP_channel_join(token, channel_id):
    # include valid token function here, stub function atm
    help.is_valid_token(token)

    # check if channel is valid
    help.check_channel_validity(channel_id)

    # check if user is a member of the channel
    help.is_user_valid_channel_member(token, channel_id)
    member_join = db.get_users_by_key('token', token)

    # checks if authorized user is admin, if not channel is private
    help.is_slackr_admin(token)

    # adds user to members list in channel
    members = DATABASE['channels'][channel_id]['members']
    members.append(dict(member_join))

    return {
    }


def is_channel_owner(channel, u_id):
    """
    Returns boolean if the user is an owner of the channel
    :param channel: dictionary for a specific channel
    :param u_id: integer for a specific user
    :return: returns boolean
    """
    # checks if authorized user is already an admin

    for members in channel["owner_members"]:
        # find the right user
        if members["u_id"] == u_id:
            return True

    return False


def channel_addowner(token, channel_id, u_id):
    """
    Adds the user with the given u_id as an owner
    :param token: authorised user's identifier
    :param channel_id: Integer for a specific channel
    :param u_id: integer for a specific user
    :return: returns an empty dictionary
    """
    # include valid token function here, stub function atm
    help.is_valid_token(token)

    # check if channel is valid
    help.check_channel_validity(channel_id)

    # check if user is channel owner
    if not db.is_owner_in_channel("token", token, channel_id):
        raise AccessError("You are not the channel owner, so don't have permission!")

    channel = db.get_channels_by_key("channel_id", channel_id)[0]
    # checks if authorized user is already an admin
    if is_channel_owner(channel, u_id):
        raise InputError(f"User with user_id {u_id} is already the channel owner")

    user = db.get_users_by_key("u_id", u_id)[0]
    if not db.is_user_in_channel("u_id", u_id, channel_id):
        channel["members"].append(user)


    channel["owner_members"].append(user)

    return {
    }


def channel_removeowner(token, channel_id, u_id):
    """
    Removes the user with u_id from being an owner
    :param token: authorised user's identifier
    :param channel_id: Integer for a specific channel
    :param u_id: integer for a specific user
    :return: returns an empty dictionary
    """
    # include valid token function here, stub function atm
    help.is_valid_token(token)

    # check if channel is valid
    help.check_channel_validity(channel_id)

    # check if user is channel owner
    if not db.is_owner_in_channel("token", token, channel_id):
        raise AccessError("You are not the channel owner, so don't have permission!")

    # check if user is a member of the channel
    if not db.is_owner_in_channel("u_id", u_id, channel_id):
        raise InputError("User is not owner")

    # checks if authorized user is already an admin
    channel = db.get_channels_by_key("channel_id", channel_id)[0]

    if not is_channel_owner(channel, u_id):
        raise InputError(f"User with {u_id} was not a channel owner")

    user = db.get_users_by_key("u_id", u_id)[0]
    channel["owner_members"].remove(user)

    return {
    }
