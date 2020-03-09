import channels as c
import helper_functions.channel_helpers as ch

# every token should print out the list of all channels
def test_channels_listall():
    assert c.channels_listall(ch.chan_owner_token) == [{'ch.chan_owner_id': 1, 'name': "channel1"}, {'ch.private_channel_id': 1, 'name': "channel2"}]

    assert c.channels_listall(ch.slackr_owner_token) == [{'ch.chan_owner_id': 1, 'name': "channel1"}, {'ch.private_channel_id': 1, 'name': "channel2"}]

    assert c.channels_listall(ch.member_token) == [{'ch.chan_owner_id': 1, 'name': "channel1"}, {'ch.private_channel_id': 1, 'name': "channel2"}]

