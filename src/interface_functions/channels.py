from error import InputError
import time
import database_files.database_retrieval as db
from database_files.database_retrieval import get_user_channels_by_key
from database_files.database_retrieval import get_channels

def channels_list(token):
    # Raise an access error if not a valid token
    # TODO

    # Get the list of all channels the user is part of
    channels = get_user_channels_by_key("token", token)

    # return the list
    return {"channels": channels}


def channels_listall(token):
    # Raise an access error if not a valid token
    # TODO

    # Get the list of all channels the user is part of
    channels = get_channels()

    # return the list
    return {"channels": channels}


def channels_create(token, name, is_public):
    if len(name) > 20:
        raise InputError("Channel name cannot be more than 20 characters long")

    channels = db.get_channels()
    user = db.get_users_by_key("token", token)[0]
    channel_id = time.time()

    channels.append(
        {
            "channel_id": channel_id,
            "name": name,
            "owner_members": [user],
            "members": [user],
            "standup": {"active": False, "msg_queue": "", "time_finish": None},
            "is_public": is_public
        }
    )

    return {"channel_id": channel_id}
