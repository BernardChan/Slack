# pylint: disable=W0105, W0622, W0603
import threading
import time
import sched
import database_files.database_retrieval as db
import helper_functions.interface_function_helpers as help
from error import InputError


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
    # Get the messages list from the database and append the current message to it
    messages = db.get_messages()
    user = db.get_users_by_key("token", token)[0]

    messages.insert(0, {
        "message_id": message_id,
        "u_id": user["u_id"],
        "message": message,
        "time_created": message_id,
        "reacts": {"react_id": None, "u_ids": [], "is_this_user_reacted": False},
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
    help.check_message_length(message)
    help.check_member_status_of_channel(token, channel_id)

    # Get the messages list from the database and append the current message to it
    message_id = help.get_unique_id()

    insert_message(token, channel_id, message, message_id)

    return {
        'message_id': message_id,
    }


def message_remove(token, message_id):
    """

    :param token:
    :param message_id:
    :return:
    """
    return "Not Implemented"


def message_edit(token, message_id, message):
    """

    :param token:
    :param message_id:
    :param message:
    :return:
    """
    return "Not Implemented"


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


def message_react(token, message_id, react_id):
    return "Not Implemented"


def message_unreact(token, message_id, react_id):
    return "Not Implemented"
