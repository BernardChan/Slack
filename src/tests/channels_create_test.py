import helper_functions.test_helper_file as ch
from interface_functions import channels


def test_channels_create():
    is_public = False
    assert channels.channels_create(ch.chan_owner_token, ch.channel_name, is_public) == ch.channel_id
    is_public = True
    assert channels.channels_create(ch.chan_owner_token, ch.channel_name, is_public) == ch.private_channel_id
    if len(ch.channel_name) > 20:
        raise(InputError)
        
        
