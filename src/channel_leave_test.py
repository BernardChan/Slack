# Tests for the leave() function in channel.py
# Dependencies on:
#   auth_register()
#   channel_details()
#   channel_invite()

import pytest
from channel import channel_invite
from channel import channel_leave as leave
from error import InputError, AccessError
import channel_helpers as ch


###############################
#            Tests            #
###############################

# Helper function that asserts that a member left a channel
def assert_user_leave(user_token, user_id):
    # Check that user is actually part of the channel - if this fails, problem with dependencies
    assert(ch.is_member(user_id))

    leave(user_token, ch.channel_id)

    # Assert that user is no longer a member
    assert(not ch.is_member(user_id))


# Check that the slackr owner may leave a channel
def test_leave_slackr_owner():

    # Invite the slackr owner to the channel
    channel_invite(ch.chan_owner_token, ch.channel_id, ch.slackr_owner_id)

    # Assert the slackr owner is not a member of the channel
    assert_user_leave(ch.slackr_owner_token, ch.slackr_owner_id)


# Check that the channel owner may leave a channel
def test_leave_channel_owner():

    # Assert channel owner is not a member of the channel
    assert_user_leave(ch.chan_owner_token, ch.chan_owner_id)


# Check that a non-owner member may leave
def test_leave_member():

    # Invite a normal member to the channel
    channel_invite(ch.chan_owner_token, ch.channel_id, ch.member_id)

    assert_user_leave(ch.member_token, ch.member_id)


# Test if AccessError exceptions are raised
# Should raise exception when:
#   User is not authorised (token invalid)
#   Authorised User is not a member of the channel_id (but channel_id exists)
def test_leave_access_error():
    assert(not ch.is_member(ch.chan_owner_id))

    # User is not part of a channel, raise AccessError exception
    with pytest.raises(AccessError):
        leave(ch.chan_owner_token, ch.channel_id)

    # User does not exist, raise AccessError
    with pytest.raises(AccessError):
        leave("INVALIDTOKEN", ch.channel_id)


# Test if InputError's are raised
# Should raise when:
#   channel_id does not exist
def test_leave_input_error():

    # Channel does not exist, raise InputError
    with pytest.raises(InputError):
        leave(ch.slackr_owner_id, -100000)
