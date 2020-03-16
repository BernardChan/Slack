from interface_functions import channels as c
import helper_functions.test_helper_file as ch

def test_channels_list():
    
    # checks channels list for a channel owner token
    assert c.channels_list(ch.chan_owner_token) == [{'ch.channel_id': 1, 'name': "channel1"}, {'ch.private_channel_id': 1, 'name': "channel2"}]
    
    # gives empty channel list for default member
    assert c.channels_list(ch.member_token) == {}    
    
    # empty channel list for slackr owner
    assert c.channels_list(ch.slackr_owner_token) == {}
