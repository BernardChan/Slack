#
# messages = [
#     {
#         "message_id": 0,
#         "u_id": 1,
#         "message": "hello",
#         "time_created": 1,
#         "reacts": None,
#         "is_pinned": False,
#         "channel_id": 0
#     },
#     {
#         "message_id": 2,
#         "u_id": 1,
#         "message": "ahello",
#         "time_created": 2,
#         "reacts": None,
#         "is_pinned": False,
#         "channel_id": 0
#     }
# ]


# Sorts by time_created
# Can be altered to accept any parameter and sort by that if needed
def sort_messages(messages):
    messages.sort(key=lambda message: message["time_created"])


def search(token, query_str):
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
