# Creates a new channel with that name that is either a public or private channel

from error import InputError
import time
import database_files.database_retrieval as db


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
            "members": [user],
            "standup": {"active": False, "msg_queue": "", "time_finish": None},
            "is_public": is_public
        }
    )

    return {"channel_id": channel_id}
