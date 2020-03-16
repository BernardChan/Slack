# TODO: move set_standup (changes "standup": Boolean in channel's dictionary) to database
# TODO: add a key for "standup_queue": [] to standups
# TODO: standup_queue's array contains dict {"message": "string", "token": int}
# TODO: create a function that lets me retrieve the standup_queue
import threading
import message_send  # TODO: import it from wherever it is


# TODO Sets the standup tag on the given channel_id to boolean
#   Throws InputError if "standup" was already True
def set_standup(channel_id, is_active):
    pass


# Sends the collected messages to the channel
def start_standup(channel_id):

    # Set "standup" key to False
    set_standup(channel_id, False)
    standup_queue = get_standup_queue()

    for message_dict in standup_queue:
        message = message_dict["message"]
        token = message_dict["token"]
        message_send(token, channel_id, message)



def standup_start(token, channel_id, length):

    # Set the "standup" key on channel dict to True to show a standup has started
    set_standup(channel_id, True)

    # Set the "standup" key on channel dict to False after length seconds
    t = threading.Timer(length, start_standup, [channel_id])
    t.start()


if __name__ == "__main__":
    standup_start(0, 10, 5)