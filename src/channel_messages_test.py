# Tests for the channel_messages function in channel.py

# NOTE: channel_messages(token, channel_id, start)

# Dependencies:


import pytest
from channel import channel_messages
from error import InputError, AccessError
import helper_functions.channel_helpers as ch


def test_channel_messages_success():
    pass

# Access error when used with invalid token
def test_profile_sethandle_access_error():

    # Raise error if invalid token
    with pytest.raises(AccessError) as e:
        channel_messages("INVALIDTOKEN", ch.channel_id, 0)
