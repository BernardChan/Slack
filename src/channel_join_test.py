# Tests for the channel_join() function in channel.py
# Dependencies:
#   auth_register()
#   channel_details()
#   channel_invite()
#   channels_create()

import pytest
from channel import channel_join as join
import channel
from error import InputError, AccessError
import channel_helpers as ch


# Helper function to check if a member joined successfully
def assert_user_join(user_token, user_id, is_public):

    # Check that user joined the channel properly
    join(user_token, ch.channel_id) if is_public else join(user_token, ch.private_channel_id)
    assert(ch.is_member(user_id, is_public))


# Check that nothing happens when a user tries to join a channel they are already in
def test_join_existing():

    # Invite the slackr_owner and member to the public and private channels
    channel.channel_invite(ch.chan_owner_token, ch.channel_id, ch.member_id)
    channel.channel_invite(ch.chan_owner_token, ch.private_channel_id, ch.member_id)
    channel.channel_invite(ch.chan_owner_token, ch.channel_id, ch.slackr_owner_id)
    channel.channel_invite(ch.chan_owner_token, ch.private_channel_id, ch.slackr_owner_id)

    # Assert program does not throw exceptions when users are already part of the channel
    assert_user_join(ch.slackr_owner_token, ch.slackr_owner_id, True)
    assert_user_join(ch.slackr_owner_token, ch.slackr_owner_id, False)
    assert_user_join(ch.slackr_owner_token, ch.member_id, True)
    assert_user_join(ch.slackr_owner_token, ch.member_id, False)
    assert_user_join(ch.slackr_owner_token, ch.chan_owner_id, True)
    assert_user_join(ch.slackr_owner_token, ch.chan_owner_id, False)


# Check that a normal user can join a public channel
def test_join_member():
    assert_user_join(ch.member_token, ch.member_id, True)


# Check that the slackr owner can join a public and private channel
def test_join_slackr_owner():
    assert_user_join(ch.slackr_owner_token, ch.slackr_owner_id, True)
    assert_user_join(ch.slackr_owner_token, ch.slackr_owner_id, False)


# Check that AccessError is thrown when
#   channel_id is private and user is not admin
#   user is not authorised
def test_join_access_error():
    assert(not ch.is_member(ch.member_id, True))

    # User is not admin and attempts to join a private channel
    with pytest.raises(AccessError):
        join(ch.member_id, ch.private_channel_id)

    # User does not exist, raise AccessError
    with pytest.raises(AccessError):
        join("INVALIDTOKEN", ch.channel_id)


# Check that InputError exception is thrown when channel_id does not exist
def test_join_input_error():

    # Channel does not exist, raise InputError
    with pytest.raises(InputError):
        join(ch.member_id, -100000)
