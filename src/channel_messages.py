# Function implementation for channel/messages(token, channel_id, start)

import database_files.database_retrieval as db
import helper_functions.interface_function_helpers as help
from error import InputError


# Finish is the ending index for the list slice, whereas
# end is the ending NUMBER to be returned by messages
# can't use -1 for slice notation since that return (n-1)th place
def get_finish_and_end(start, messages):
    end = start + 50
    finish = end
    num_messages = len(messages)
    if start >= num_messages:
        raise InputError("Start given was greater than the number of messages in the channel")

    # set finish to -1 if we don't have 50 messages to send back
    if num_messages < end:

        end = -1

    if end == -1:
        finish = len(messages)

    return finish, end


def channel_messages(token, channel_id, start):

    # Check Errors
    help.check_channel_validity(channel_id)
    help.is_user_valid_channel_member(token, channel_id)

    messages = db.get_channel_messages(channel_id)

    # Get the finish index for messages and end index for return value
    finish, end = get_finish_and_end(start, messages)

    return {
        "messages": messages[start: finish],
        "start": start,
        "end": end,
    }
