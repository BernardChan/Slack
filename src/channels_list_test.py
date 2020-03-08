import channels
import channel_helpers as ch

def test_channels_list():
    
    # checks channels list for a channel owner token
    assert channels_list(ch.chan_owner_token) == 
    [{ch.channel_id, "channel1"}, {ch.private_channel_id, "channel2"}]
    
    # gives empty channel list for default member
    assert channels_list(ch.member_token) == {}    
    
    # empty channel list for slackr owner
    assert channels_list(ch.slackr_owner_token) == {}
