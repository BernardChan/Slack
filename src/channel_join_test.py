# Tests for the channel_join() function in channel.py
# Dependencies:
#   auth_register()
#   channel_details()
#   channel_invite()
#   channels_create()
# TODO: dependencies
# TODO: assert before/after function to check if user successfully did not exist/did join

import pytest
from channel import channel_join as join
from error import InputError, AccessError
import channel_helpers as ch


# Helper function to check if a member joined successfully
def assert_user_join(user_token, user_id):

    # Check that user is not a member of the channel already
    assert(not ch.is_member(user_id, True))

    # Check that user joined the channel properly
    join(user_token, ch.channel_id)
    assert(ch.is_member(user_id, True))


# Check that nothing happens when a user tries to join a channel they are already in
def test_join_existing():
    pass


# Check that a normal user can join a public channel
def test_join_member():
    assert_user_join(ch.member_token, ch.member_id)


# Check that the slackr owner can join a public channel
def test_join_admin_public():
    assert_user_join(ch.slackr_owner_token, ch.member_id)


# Check that the slackr owner can join a private channel
def test_join_admin_private():
    pass


# Check that InputError exception is thrown when channel_id does not exist
def test_join_input_error():
    pass


# Check that AccessError is thrown when
#   channel_id is private and user is not admin
#   user is not authorised
def test_join_access_error():
    pass
