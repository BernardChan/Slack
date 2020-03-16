from database_files.database_retrieval import get_user_channels_by_key, get_channel_messages


# Sorts by time_created
# Can be altered to accept any parameter and sort by that if needed
def sort_messages(messages):
    messages.sort(key=lambda message: message["time_created"])


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


# For initial testing
if __name__ == "__main__":
    messages = search(0, "str") # return message_id = 1, message_id = 0
    print(messages)
