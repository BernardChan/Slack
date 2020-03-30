import pytest
from error import AccessError
from interface_functions import channels as c
import helper_functions.test_helper_file as ch

"""
def test_channels_list():
    
    # checks channels list for a channel owner token
    assert c.channels_list(ch.chan_owner_token) == [{'ch.channel_id': 1, 'name': "channel1"}, {'ch.private_channel_id': 1, 'name': "channel2"}]
    
    # gives empty channel list for default member
    assert c.channels_list(ch.member_token) == {}    
    
    # empty channel list for slackr owner
    assert c.channels_list(ch.slackr_owner_token) == {}
"""

def test_channels_list_success():
    chan_list = c.channels_list(ch.chan_owner_token)["channels"]
    assert len(chan_list) == 2
    assert chan_list[0]["channel_id"] == ch.channel_id
    assert chan_list[1]["channel_id"] == ch.private_channel_id
    
    for channel in chan_list:
        if channel["channel_id"] == ch.channel_id:
            assert channel["name"] == "channel1"
        if channel["channel_id"] == ch.private_channel_id:
            assert channel["name"] == "channel1"

def test_channels_list_access_error():
    with pytest.raises(AccessError):
        c.channels_list("INVALIDTOKEN")