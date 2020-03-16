# Tests for the channel_leave() function in channel.py
# Tests include checking:
#   slackr_owner/channel_owner/non-owner_member can leave a public/private channel (6 tests)
#   InputError when:
#       channel_id does not exist
#   AccessError when:
#       User is not authorised (token invalid)
#       Authorised User is not a member of the channel_id (but channel_id exists)

# Function dependencies on:
#   auth_register()
#   channel_details()
#   channel_invite()
#   channels_create()

import pytest
from interface_functions.channel import channel_invite
from interface_functions.channel import channel_leave as leave
from error import InputError, AccessError
import helper_functions.test_helper_file as ch


# Helper function that asserts that a member left a channel
def assert_user_leave(user_token, user_id, is_public):
    # Check that user is actually part of the channel - if this fails, problem with dependencies
    assert(ch.is_member(user_id, is_public))

    leave(user_token, ch.channel_id) if is_public else leave(user_token, ch.private_channel_id)

    # Assert that user is no longer a member
    assert(not ch.is_member(user_id, is_public))


###############################
#            Tests            #
###############################

# Check that the slackr owner may leave a channel
def test_leave_slackr_owner():

    # Invite the slackr owner to the public and private channel
    channel_invite(ch.chan_owner_token, ch.channel_id, ch.slackr_owner_id)
    channel_invite(ch.chan_owner_token, ch.private_channel_id, ch.slackr_owner_id)

    # Assert the slackr owner is not a member of the public or private channels
    assert_user_leave(ch.slackr_owner_token, ch.slackr_owner_id, True)
    assert_user_leave(ch.slackr_owner_token, ch.slackr_owner_id, False)


# Check that the channel owner may leave a channel
def test_leave_channel_owner():

    # Assert channel owner is not a member of the public or private channels
    assert_user_leave(ch.chan_owner_token, ch.chan_owner_id, True)
    assert_user_leave(ch.chan_owner_token, ch.chan_owner_id, False)


# Check that a non-owner member may leave
def test_leave_member():

    # Invite a normal member to both the public and private channel
    channel_invite(ch.chan_owner_token, ch.channel_id, ch.member_id)
    channel_invite(ch.chan_owner_token, ch.private_channel_id, ch.member_id)

    # Assert member is not a member of public or private channels
    assert_user_leave(ch.member_token, ch.member_id, True)
    assert_user_leave(ch.member_token, ch.member_id, False)


# Test if AccessError exceptions are raised
# Should raise exception when:
#   User is not authorised (token invalid)
#   Authorised User is not a member of the channel_id (but channel_id exists)
def test_leave_access_error():
    assert(not ch.is_member(ch.member_id, True))

    # User is not part of the channel, raise AccessError exception
    with pytest.raises(AccessError):
        leave(ch.member_id, ch.channel_id)

    # User does not exist, raise AccessError
    with pytest.raises(AccessError):
        leave("INVALIDTOKEN", ch.channel_id)


# Test if InputError's are raised
# Should raise when:
#   channel_id does not exist
def test_leave_input_error():

    # Channel does not exist, raise InputError
    with pytest.raises(InputError):
        leave(ch.chan_owner_id, -100000)
