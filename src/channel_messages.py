# Function implementation for channel/messages(token, channel_id, start)

# TODO: Create function stubs in database that just gives us an interface to get data from DATABASE
# if database structure changes, only the function has to be changed


# Finish is the ending index for the list slice, whereas
# end is the ending NUMBER to be returned by messages
# can't use -1 for slice notation since that return (n-1)th place
def get_finish_and_end(start, messages):
    end = start + 50
    finish = end

    # set finish to -1 if we don't have 50 messages to send back
    if len(messages) < end:
        print("no more messages to display")
        end = -1

    if end == -1:
        finish = len(messages)

    return finish, end


def channel_messages(token, channel_id, start):
    # TODO: get messages

    # Get the finish index for messages and end index for return value
    finish, end = get_finish_and_end(start, messages)

    return {
        "messages": messages[start: finish],
        "start": start,
        "end": end,
    }
