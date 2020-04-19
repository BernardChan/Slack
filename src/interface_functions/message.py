# pylint: disable=W0105, W0622, W0603
import threading
import time
import sched
import database_files.database_retrieval as db
import helper_functions.interface_function_helpers as help
from error import InputError, AccessError


"""
File for functions relating to messages in Slackr
"""


def insert_message(token, channel_id, message, message_id):
    """
    Inserts the given message into the database
    :param token: authorised user's identifier
    :param channel_id: Integer for a specific channel
    :param message: string for message to be sent to a channel
    :param message_id: Integer for a unique identifier of the message
    :return: returns nothing
    """
    help.is_valid_token(token)
    # Get the messages list from the database and append the current message to it
    messages = db.get_messages()
    user = db.get_users_by_key("token", token)[0]

    messages.insert(0, {
        "message_id": message_id,
        "u_id": user["u_id"],
        "message": message,
        "time_created": message_id,
        "reacts": [],
        "is_pinned": False,
        "channel_id": channel_id,
        })


def message_send(token, channel_id, message):
    """
    Sends a given message by the token owner to the given channel
    :param token: authorised user's identifier
    :param channel_id: Integer for a specific channel
    :param message: string for message to be sent to a channel
    :return: returns dictionary with the generated message_id for the message
    """
    # Error checking
    help.is_valid_token(token)
    help.check_message_length(message)
    help.check_member_status_of_channel(token, channel_id)

    # Get the messages list from the database and append the current message to it
    message_id = help.get_unique_id()

    insert_message(token, channel_id, message, message_id)

    return {
        'message_id': message_id,
    }


def is_valid_message_change(user, message):
    # Authorised user did not make the message and is not the owner
    if user["u_id"] != message["u_id"] and user["permission_id"] != 1:
        raise AccessError("You are not authorised to delete this message")


def is_valid_message_id(message):
    if len(message) == 0:
        raise InputError("Message Not found")


def message_remove(token, message_id):

    help.is_valid_token(token)

    message = db.get_messages_by_key("message_id", message_id)

    # Raise errors
    is_valid_message_id(message)
    user = db.get_users_by_key("token", token)[0]
    message = message[0]
    is_valid_message_change(user, message)

    # Remove the message
    messages = db.get_messages()
    messages.remove(message)

    return {}


# Assumption - input error raised if message not found
def message_edit(token, message_id, message):
    
    help.is_valid_token(token)

    message_string = message

    message = db.get_messages_by_key("message_id", message_id)

    # Raise errors
    is_valid_message_id(message)
    user = db.get_users_by_key("token", token)[0]
    message = message[0]
    is_valid_message_change(user, message)

    message["message"] = message_string  # TODO: verify this works

    return {}


# File for message/sendlater(token, channel_id, message, time_sent)
# Will use a POST request

# Dependencies:
# - message_send()

# Message queue for sending a message later
Q = []
DO_WORK = threading.Event()


# Dequeues send_later_queue whenever a new item is added to it
def set_sched():
    """
    Dequeues the send later message queue containing all the messages to be sent at a later date
    :return: returns nothing
    """
    global Q, DO_WORK
    while True:

        # If there are items to dequeue
        if Q:

            # get the time_sent, message and priority from send_later_queue
            time_sent = Q[0]["time_sent"]
            message = Q[0]["message"]
            priority = Q[0]["priority"]
            token = Q[0]["token"]
            channel_id = Q[0]["channel_id"]
            message_id = Q[0]["message_id"]

            del Q[0]

            # Create a schedule object to be run at a later date
            sch = sched.scheduler(time.time, time.sleep)
            sch.enterabs(
                time_sent,
                priority,
                insert_message, [token, channel_id, message, message_id]
            )
            sch.run()
        else:
            DO_WORK = threading.Event()
            DO_WORK.wait()


# Adds a message to be sent at a later date
def send_later(token, channel_id, message, time_sent):
    """
    Sends a message at the designated time
    :param token: authorised user's identifier
    :param channel_id: Integer for a specific channel
    :param message: String for the message to be sent
    :param time_sent: unix time for when the message should be sent
    :return: returns dictionary with the message_id
    """
    help.is_valid_token(token)
    help.is_message_valid(token, message, channel_id)
    message_id = help.get_unique_id()
    curr = time.time()
    if time_sent - curr < 0:
        raise InputError("Time given was in the past")

    global DO_WORK
    Q.append(
        {"message": message,
         "time_sent": time_sent,
         "priority": time.time(),
         "token": token,
         "channel_id": channel_id,
         "message_id": message_id
         })
    DO_WORK.set()

    return {"message_id": message_id}


def message_pin(token, message_id):
    
    help.is_valid_token(token)

    message = db.get_messages_by_key("message_id", message_id)

    # Error Checking
    is_valid_message_id(message)
    help.is_slackr_admin(token)
    message = message[0]
    if message["is_pinned"]:
        raise InputError("Message already pinned")

    channel_id = message["channel_id"]
    help.is_user_valid_channel_member(token, channel_id)

    # Pin the message
    message["is_pinned"] = True
    return {}


def message_unpin(token, message_id):
    
    help.is_valid_token(token)

    message = db.get_messages_by_key("message_id", message_id)

    # Error Checking
    is_valid_message_id(message)
    help.is_slackr_admin(token)
    message = message[0]
    if not message["is_pinned"]:
        raise InputError("Message already pinned")

    channel_id = message["channel_id"]
    help.is_user_valid_channel_member(token, channel_id)

    # Pin the message
    message["is_pinned"] = False
    return {}


def is_valid_react(react_id):
    if react_id != 1:
        raise InputError


def get_react_by_key(key, value, message):
    reacts = message["reacts"]
    for react in reacts:
        if react[key] == value:
            return react
    return None

def is_already_reacted(message, react_id, user_id):
    react = get_react_by_key("react_id", react_id, message)

    # No reacts exist yet
    if react is None:
        return False
    if react["react_id"] == react_id and user_id in react["u_ids"]:
        return True

    return False


def message_react(token, message_id, react_id):
    
    help.is_valid_token(token)

    message = db.get_messages_by_key("message_id", message_id)

    # Error checking
    is_valid_message_id(message)
    message = message[0]
    channel_id = message["channel_id"]
    help.is_user_valid_channel_member(token, channel_id)
    is_valid_react(react_id)
    user = db.get_users_by_key("token", token)[0]

    if is_already_reacted(message, react_id, user["u_id"]):
        raise InputError("You have already reacted to this")

    react = get_react_by_key("react_id", react_id, message)
    if react is None:
        message["reacts"].append(
            {"react_id": react_id,
             "u_ids": [user["u_id"]],
             "is_this_user_reacted": True})
    else:
        react["u_ids"].append(user["u_id"])
        react["is_this_user_reacted"] = True

    return {}


def message_unreact(token, message_id, react_id):
    
    help.is_valid_token(token)
    
    print(f"message id was {message_id}")
    message = db.get_messages_by_key("message_id", message_id)
    print(f"message returned was {message}")
    # Error checking
    is_valid_message_id(message)
    message = message[0]
    channel_id = message["channel_id"]
    help.is_user_valid_channel_member(token, channel_id)
    is_valid_react(react_id)
    user = db.get_users_by_key("token", token)[0]

    if not is_already_reacted(message, react_id, user["u_id"]):
        raise InputError("You have not reacted to this")

    react = get_react_by_key("react_id", react_id, message)
    react["u_ids"].remove(user["u_id"])
    if len(react["u_ids"]) == 0:
        message["reacts"].remove(react)

    return {}
