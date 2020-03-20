# Appends to the standup dictionary's "msg_queue"
# Formats the message so that it can just be directly sent by standup_active's thread

import database_files.database_retrieval as db
import helper_functions.interface_function_helpers as help
from error import InputError


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


