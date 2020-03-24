# Given a Channel with ID channel_id that the authorised user is part of, provide basic details about the channel

import database_files.database_retrieval as db
import helper_functions.interface_function_helpers as help


def channel_details(token, channel_id):
    help.check_channel_validity(channel_id)
    help.check_member_status_of_channel(token, channel_id)

    channel = db.get_channels_by_key("channel_id", channel_id)[0]

    return {
        "name": channel["name"],
        "owner_members": channel["owner_members"],
        "all_members": channel["members"]
    }
