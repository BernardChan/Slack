# Function for standup_start

import threading
from interface_functions.message import message_send
from database_files.database import DATABASE
import database_files.database_retrieval as db
from helper_functions.interface_function_helpers import check_channel_validity
from error import InputError
import time

# Sets the standup tag on the given channel_id to True/False (is_active)
# Throws InputError if channel["standup"] was already True AND we're trying to set it as True
def set_standup(channel_id, is_active):

    # Find the channel with channel_id
    channel = db.get_channels_by_key("channel_id", channel_id)[0]

    if channel["standup"]["active"] and is_active:
        raise InputError("Standup was already active")
    else:
        channel["standup"]["active"] = is_active


# Sends the collected messages to the channel
def end_standup(token, channel_id):

    # Set "standup" key to False
    set_standup(channel_id, False)
    standup_message = db.get_channel_standup(channel_id)  # TODO: standup send needs to access this as well
    message_send(token, channel_id, standup_message["msg_queue"])


# Works by:
# 1. Setting channel["standup"]["active"] to True (designates a standup is active)
# 2. Creates a thread that has a timer of `length` seconds long
# 3. After `length` seconds have elapsed, end_standup is executed and the message in
#   channel["standup"]["msg_queue"] is sent using the user's token.
def standup_start(token, channel_id, length):
    check_channel_validity(channel_id)
    # Set the "standup" key on channel dict to True to show a standup has started
    set_standup(channel_id, True)

    # Set the "standup" key on channel dict to False after length seconds
    t = threading.Timer(length, end_standup, [token, channel_id])
    t.start()

    return time.time() + length


if __name__ == "__main__":
    print([d["standup"] for d in DATABASE["channels"][0:]])
    standup_start(1, 0, 4)
    print([d["standup"] for d in DATABASE["channels"][0:]])
