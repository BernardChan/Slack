from database_files.database_retrieval import get_user_channels_by_key, get_channel_messages
from helper_functions.interface_function_helpers import is_valid_token
from database_files.database_retrieval import get_users


# USERS/ALL
# Provides a list of all users and their respective details
# Only raises AccessError for invalid token
def users_all(token):

    # Raise an access error if not a valid token
    is_valid_token(token)

    # Get the list of all users
    users = get_users()
    # return the list
    return {"users": users}


# Sorts by time_created
# Can be altered to accept any parameter and sort by that if needed
def sort_messages(messages):
    messages.sort(key=lambda message: message["time_created"])

import database_files.database as db
# Searches by:
# 1. Getting the user's list of channels
# 2. Getting the messages that are in those channels
# 3. Returning only the ones with the query_str in it
def search(token, query_str):

    user_channels = get_user_channels_by_key("token", token)
    found_messages = []

    # Get the messages from each channel the user is part of
    for channel in user_channels:
        messages = get_channel_messages(channel["channel_id"])

        # Return the messages matching the query_str
        for message in messages:
            if query_str in message["message"]:
                found_messages.append(message)

    # Technically unneeded but it's here for safety
    # Assumption should be that the messages are returned in order (since they're appended in order)
    # Should be n average insertion sort since it is largely sorted
    sort_messages(found_messages)
    return {"messages": found_messages}