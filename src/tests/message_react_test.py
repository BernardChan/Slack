# Tests for message_react() function in message.py
# Dependencies:
    # auth_register()
    # channels_create()
    # message_send
    # channel_messages
   
import pytest

from interface_functions.auth import auth_register
from interface_functions.message import message_send, message_react
from interface_functions.channel import channel_messages
from interface_functions.channels import channels_create
from error import InputError, AccessError

# Pytest fixture to register a test user, create a channel and send a message
@pytest.fixture
def data():
    # register a user
    user = auth_register("test.user1@test.com", "password123", "fname1", "lname1")
    u_id = user["u_id"]
    token = user["token"]
    # create a public channel, assumes that user automatically joins and is owner of that channel
    channel = channels_create(token, "newchannel", True)
    ch_id = channel["channel_id"]
    # send a message
    message = message_send(token, ch_id, "Hello world!")
    message_id = message["message_id"]

    return {
        "u_id": u_id,
        "token": token,
        "ch_id": ch_id,
        "message_id": message_id,
    }

# helper function to assert that a message has been reacted to
def assert_is_reacted(token, user_id, channel_id, message_id):
    # channel messages returns a dictionary containing messages, start, end
    messages = channel_messages(token, channel_id, 0)["messages"]
    # messages is a list of dictionaries containing message_id, u_id, message, time_created, reacts, is_pinned
    # find the message with message_id and assert that its reacted with react id 1 and the given u_id
    for message in messages:
        if message["message_id"] == message_id:
            # reacts is a list of dictionaries where each dictionary contains react_id, u_id, is_this_user_reacted
            assert(message["reacts"][0]["react_id"] == 1)
            assert(message["reacts"][0]["u_id"] == user_id)

# test succesful
def test_message_react_success(data):
    # data fixture creates a user and channel then sends a message with message_id
    # save this data
    u_id = data["u_id"]
    token = data["token"]
    ch_id = data["ch_id"]
    message_id = data["message_id"]
    # react to the message
    message_react(token, message_id, 1)
    # assert message was reacted
    assert_is_reacted(token, u_id, ch_id, message_id)

# test for input errors
def test_message_react_input_errors(data):
    # CREATE A USER AND CHANNEL, SEND A MESSAGE
    # save required data variables
    token = data["token"]
    message_id = data["message_id"]

    # INVALID MESSAGE_ID
    with pytest.raises(InputError):
        message_react(token, -1000, 1)

    # INVALID REACT_ID (any react_id that isn't 1)
    with pytest.raises(InputError):
        message_react(token, message_id, 5)

    # MESSAGE ALREADY CONTAINS AN ACTIVE REACT FROM THE USER
    # react to the message correctly
    message_react(token, message_id, 1)
    # try reacting again
    with pytest.raises(InputError):
        message_react(token, message_id, 1)


# test for access error from invalid token
def test_message_react_invalid_token(data):
    # CREATE A USER AND CHANNEL, SEND A MESSAGE
    # save required data variables (only needs message id)
    message_id = data["message_id"]

    # INVALID TOKEN
    with pytest.raises(AccessError):
        message_react("INVALIDTOKEN", message_id, 1)
