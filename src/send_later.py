# File for message/sendlater(token, channel_id, message, time_sent)
# Will use a POST request

# Dependencies:
#   channel/details (needed to get list of members of a channel
# from channel import channel_details  # TODO: remove this if we move AccessError check to helper file
# from message import message_send
from error import InputError, AccessError
import threading
import time
import sched


# gets the user dictionary based on the key given
# If user is not found, return None
# TODO: should I make an exception or try/catch for when the wrong key_type is given?
#   e.g. f"key_type of {key_type} does not exist in the dictionary"
def get_user(key_type, key):
    for user in DATABASE["users"]:
        if user[key_type] == key:
            return user

    return None


# Returns true if a user is a part of channel_id, else false
def is_member(token, channel_id):
    # TODO: get user_id from token
    members = channel_details(token, channel_id)["all_members"]
    user = get_user("token", token)

    if user is None:
        return False

    for member in members:
        if member["u_id"] == user["u_id"]:
            return True


# Gets the dictionary containing the channel_id
# Returns the channel dictionary, or None if not found
def get_channel_with_id(channel_id):
    for channel in channels:
        if channel["channel_id"] == channel_id:
            return channel

    # Could not find the channel with channel_id
    return None


# Check is a channel_id is valid
# Returns true if it finds the channel with channel_id, else false
def channel_is_valid(channel_id):
    return True if get_channel_with_id(channel_id) else False


# Throws errors where needed
def is_message_valid(message, channel_id):
    if len(message) > 1000:
        raise InputError("Message exceeded 1000 Characters")

    elif not channel_is_valid(channel_id):
        raise InputError("The given channel_id was not found")

    # TODO: add Access Error for when a user hasn't joined a channel they're posting to


# TODO: delete this message_send and import the real one. This is for testing purposes only
def message_send(message):
    print(message)


# Message queue for sending a message later
send_later_queue = [{"message": "hi", "time_sent": time.time(), "priority": time.time()}]
do_work = threading.Event()


# TODO: import the real message_send function
# Dequeues send_later_queue whenever a new item is added to it
def set_sched():
    global send_later_queue
    global do_work
    while True:

        # If there are items to dequeue
        if send_later_queue:

            # get the time_sent, message and priority from send_later_queue
            time_sent, message, priority = send_later_queue[0]["time_sent"], send_later_queue[0]["message"], send_later_queue[0]["priority"]
            del(send_later_queue[0])

            # Create a schedule object to be run at a later date
            s = sched.scheduler(time.time, time.sleep)
            s.enterabs(time_sent, priority, message_send, [message])
            s.run()
        else:
            do_work = threading.Event()
            do_work.wait()


# TODO: move this to server.py
# Creates a thread for setting a schedule
def start_thread_helper():
    t = threading.Thread(target=set_sched)
    t.start()


# TODO: add error checking
# Adds a message to be sent at a later date
def send_later(token, channel_id, message, time_sent):
    # is_message_valid(message, channel_id)
    global do_work
    send_later_queue.append({"message": message, "time_sent": time_sent, "priority": time.time()})
    do_work.set()


if __name__ == "__main__":
    start_thread_helper()  # Should only be called once
    curr = time.time()
    for i in range(100):
        send_later(0, 0, str(i), curr + 5)

    time.sleep(20)
    send_later(0, 0, "yoyoyo", time.time())

