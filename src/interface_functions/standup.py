import helper_functions.interface_function_helpers as help
import database_files.database_retrieval as db
from interface_functions.message import message_send
from helper_functions.interface_function_helpers import check_channel_validity
from error import InputError
import time
import threading

# TODO: Add AccessErrors


# Sets the standup tag on the given channel_id to True/False (is_active)
# Throws InputError if channel["standup"] was already True AND we're trying to set it as True
def set_standup(channel_id, is_active, time_finish):

    # Find the channel with channel_id
    channel = db.get_channels_by_key("channel_id", channel_id)[0]

    if channel["standup"]["active"] and is_active:
        raise InputError("Standup was already active")
    else:
        channel["standup"]["active"] = is_active
        channel["standup"]["time_finish"] = time_finish


# Sends the collected messages to the channel
def end_standup(token, channel_id):

    # Set "standup" key to False
    set_standup(channel_id, False, None)
    standup_message = db.get_channel_standup(channel_id)

    messages = db.get_messages()
    message_id = time.time()
    user = db.get_users_by_key("token", token)[0]

    # Can't reuse message send due to error checking and this function behaving slightly differently
    messages.append(
        {
            "message_id": message_id,
            "u_id": user["u_id"],
            "message": standup_message["msg_queue"],
            "time_created": message_id,
            "reacts": {"react_id": None, "u_ids": [], "is_this_user_reacted": False},
            "is_pinned": False,
            "channel_id": channel_id,
        }
    )


# Works by:
# 1. Setting channel["standup"]["active"] to True (designates a standup is active)
# 2. Creates a thread that has a timer of `length` seconds long
# 3. After `length` seconds have elapsed, end_standup is executed and the message in
#   channel["standup"]["msg_queue"] is sent using the user's token.
def standup_start(token, channel_id, length):
    check_channel_validity(channel_id)
    # Set the "standup" key on channel dict to True to show a standup has started
    time_finish = time.time() + length
    set_standup(channel_id, True, time_finish)

    # Set the "standup" key on channel dict to False after length seconds
    t = threading.Timer(length, end_standup, [token, channel_id])
    t.start()

    return {"time_finish": time_finish}


# Returns info about a standup in the given channel
def standup_active(token, channel_id):

    # Check for errors
    help.check_channel_validity(channel_id)

    # Retrieve and return the relevant information from the database
    standup = db.get_channel_standup(channel_id)
    is_active = standup["active"]
    time_finish = standup["time_finish"]

    return {"is_active": is_active, "time_finish": time_finish}


def validate_active_standup(channel_id):
    channel = db.get_channels_by_key("channel_id", channel_id)[0]
    if not channel["standup"]["active"]:
        raise InputError("Attempted to send standup message while standup was not active")


# Adds given message to the standup message queue to be sent
# later when the standup finishes
def standup_send(token, channel_id, message):

    # Error check
    help.is_message_valid(token, message, channel_id)
    help.is_user_valid_channel_member(token, channel_id)
    validate_active_standup(channel_id)

    # Add the user's message to the message queue
    msg = db.get_channel_standup(channel_id)
    user = db.get_users_by_key("token", token)[0]
    msg["msg_queue"] += user["handle_str"] + " : " + message + "\n"

    return {}
