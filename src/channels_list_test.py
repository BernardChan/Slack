import channels
import channel_helpers as ch

def test_channels_list():
    global ch.chan_owner_token
    global ch.channel_id
    global ch.private_channel_id
    
    assert channels_list(ch.chan_owner_token) == 
    [{ch.channel_id, "channel1"}, {ch.private_channel_id, "channel2"}]
