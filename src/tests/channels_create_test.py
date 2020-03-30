# dependencies:
    # channels_list

import pytest
import helper_functions.test_helper_file as ch
from interface_functions import channels
from error import InputError, AccessError

"""
def test_channels_create():    
    is_public = False
    assert channels.channels_create(ch.chan_owner_token, ch.channel_name, is_public) == ch.channel_id
    is_public = True
    assert channels.channels_create(ch.chan_owner_token, ch.channel_name, is_public) == ch.private_channel_id
    if len(ch.channel_name) > 20:
        raise(InputError)
"""

def assert_channels_create_success(token, ch_id, name, is_public):
    channels_list = channels.channels_list(token)["channels"]
    for channel in channels_list:
        if channel["channel_id"] == ch_id:
            # correct name
            assert channel["name"] == name
            # correct is_public
            assert channel["is_public"] == is_public
            # assert user is member of channel
            for user in channel["members"]:
                assert user["token"] == token
            for user in channel["owner_members"]:
                assert user["token"] == token

def test_channels_create_public():
    ch.init_helper()
    # create public channel
    channel_id = channels.channels_create(ch.chan_owner_token, "NewChannel", True)["channel_id"]
    assert_channels_create_success(ch.chan_owner_token, channel_id, "NewChannel", True)

def test_channels_create_private():
    # create public channel
    channel_id = channels.channels_create(ch.chan_owner_token, "AnotherChannel", False)["channel_id"]
    assert_channels_create_success(ch.chan_owner_token, channel_id, "AnotherChannel", False)

def test_channels_create_input_error():
    # raise input error for name longer than 20 chars
    with pytest.raises(InputError):
        channels.channels_create(ch.chan_owner_token, "a"*21, True)

def test_channels_create_access_error():
    with pytest.raises(AccessError):
        channels.channels_create("INVALIDTOKEN", "WowChannell", False)