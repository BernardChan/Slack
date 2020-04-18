# Tests for the channel_join() function in channel.py
# Dependencies:
#   auth_register()
#   channel_details()
#   channel_invite()
#   channels_create()

import pytest
from interface_functions.channel import channel_join as join
from interface_functions import channel
from error import InputError, AccessError
import helper_functions.test_helper_file as ch
from interface_functions.workspace_reset import workspace_reset


# Helper function to check if a member joined successfully
def assert_user_join(user_token, user_id, is_public):    
    # Check that user joined the channel properly
    join(user_token, ch.channel_id) if is_public else join(user_token, ch.private_channel_id)
    assert(ch.is_member(user_id, is_public))


# Check that a normal user can join a public channel
def test_join_member():
    workspace_reset()
    ch.init_helper()
    assert_user_join(ch.member_token, ch.member_id, True)


# Check that the slackr owner can join a public and private channel
def test_join_slackr_owner():
    workspace_reset()
    ch.init_helper()
    assert_user_join(ch.slackr_owner_token, ch.slackr_owner_id, True)
    assert_user_join(ch.slackr_owner_token, ch.slackr_owner_id, False)


# Check that AccessError is thrown when
#   channel_id is private and user is not admin
#   user is not authorised
def test_join_access_error():
    workspace_reset()
    ch.init_helper()
    assert(not ch.is_member(ch.member_id, True))

    # User is not admin and attempts to join a private channel
    with pytest.raises(AccessError):
        join(ch.member_token, ch.private_channel_id)

    # User does not exist, raise AccessError
    with pytest.raises(AccessError):
        join("INVALIDTOKEN", ch.channel_id)


# Check that InputError exception is thrown when channel_id does not exist
def test_join_input_error():
    workspace_reset()
    ch.init_helper()
    # Channel does not exist, raise InputError
    with pytest.raises(InputError):
        join(ch.member_token, -100000)
    workspace_reset()