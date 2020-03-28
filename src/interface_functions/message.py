import time
import database_files.database_retrieval as db
import helper_functions.interface_function_helpers as help


def message_send(token, channel_id, message):

    # Error checking
    help.check_message_length(message)
    help.check_member_status_of_channel(token, channel_id)

    # Get the messages list from the database and append the current message to it
    messages = db.get_messages()
    message_id = time.time()
    user = db.get_users_by_key("token", token)[0]

    messages.insert(0, {
            "message_id": message_id,
            "u_id": user["u_id"],
            "message": message,
            "time_created": message_id,
            "reacts": {"react_id": None, "u_ids": [], "is_this_user_reacted": False},
            "is_pinned": False,
            "channel_id": channel_id,
        }
    )

    return {
        'message_id': message_id,
    }


def message_remove(token, message_id):
    return {
    }


def message_edit(token, message_id, message):
    return {
    }


def message_react(token, message_id, react_id):
    pass