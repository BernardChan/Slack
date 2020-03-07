import channels
import channel_helpers as ch

# every token should print out the list of all channels
def test_channels_listall():
    assert channels_listall(ch.chan_owner_token) == 
    [{ch.chan_owner_id, "channel1"}, {ch.private_channel_id, "channel2"}]

    assert channels_listall(ch.slackr_owner_token) == 
    [{ch.chan_owner_id, "channel1"}, {ch.private_channel_id, "channel2"}]

    assert channels_listall(ch.member_token) == 
    [{ch.chan_owner_id, "channel1"}, {ch.private_channel_id, "channel2"}]


