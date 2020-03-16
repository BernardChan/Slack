from database_files.database_retrieval import get_messages

# Sorts by time_created
# Can be altered to accept any parameter and sort by that if needed
def sort_messages(messages):
    messages.sort(key=lambda message: message["time_created"])


def search(token, query_str):

    messages = get_messages()

    found_messages = []
    for message in messages:
        if query_str in message["message"]:
            found_messages.append(message)

    # Technically unneeded but it's here for safety
    # Assumption should be that the messages are returned in order (since they're appended in order)
    # TODO: remove this at a later date
    sort_messages(found_messages)
    return {"messages": found_messages}


if __name__ == "__main__":
    messages = search(0, "hel")

    for message in messages:
        print(message)
