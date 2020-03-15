# File for message/sendlater(token, channel_id, message, time_sent)
# Will use a POST request

# Dependencies:
#   channel/details (needed to get list of members of a channel
# from channel import channel_details  # TODO: remove this if we move AccessError check to helper file
# from message import message_send
from error import InputError, AccessError
import threading
import time
import sched


channels = [
    {"channel_id": 0,
     "name": "foo"},

    {"channel_id": 1,
     "name": "bar"},

    {"channel_id": 2,
     "name": "baz"},

]
foo={ # TODO delete later
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

# Global Dictionary Containing every user in the slackr server
DATABASE = {
    "users": [
        {
            "token": "invalid toshi token",
            "u_id": 0,
            "name_first": "Toshi",
            "name_last": "Tabata",
        },
        {
            "token": "INVALID",
            "u_id": 1,
            "name_first": "Hayden",
            "name_last": "Smith",
        }
    ]
}


# gets the user dictionary based on the key given
# If user is not found, return None
# TODO: should I make an exception or try/catch for when the wrong key_type is given?
#   e.g. f"key_type of {key_type} does not exist in the dictionary"
def get_user(key_type, key):
    for user in DATABASE["users"]:
        if user[key_type] == key:
            return user

    return None


# Returns true if a user is a part of channel_id, else false
def is_member(token, channel_id):
    # TODO: get user_id from token
    members = channel_details(token, channel_id)["all_members"]
    user = get_user("token", token)

    if user is None:
        return False

    for member in members:
        if member["u_id"] == user["u_id"]:
            return True


# Gets the dictionary containing the channel_id
# Returns the channel dictionary, or None if not found
def get_channel_with_id(channel_id):
    for channel in channels:
        if channel["channel_id"] == channel_id:
            return channel

    # Could not find the channel with channel_id
    return None


# Check is a channel_id is valid
# Returns true if it finds the channel with channel_id, else false
def channel_is_valid(channel_id):
    return True if get_channel_with_id(channel_id) else False


# Throws errors where needed
def is_message_valid(message, channel_id):
    if len(message) > 1000:
        raise InputError("Message exceeded 1000 Characters")

    elif not channel_is_valid(channel_id):
        raise InputError("The given channel_id was not found")

    ## TODO: add Access Errror for when a user hasn't joined a channel they're posting to


def message_send(message):
    print(message)


def set_sched(time_sent, message):
    s = sched.scheduler(time.time, time.sleep)
    s.enterabs(time_sent, 0, message_send, [message])
    s.run()


def send_later(token, channel_id, message, time_sent):
    is_message_valid(message, channel_id)

    t = threading.Thread(target=set_sched, args=(time_sent, message))
    t.start()


if __name__ == "__main__":
    send_later(0,0, "2", time.time() + 10)  # sends this second
    send_later(0,0, "1", time.time() + 5)  # sends this first
