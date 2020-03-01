# Tests for the leave() function in channel.py
# Dependencies on:
#   auth_register()
#   channel_details()
#   channel_invite()

import pytest
import channel as ch
from channel import channel_leave as leave
from error import InputError, AccessError
import channel_helpers as help


###############################
#            Tests            #
###############################

# Check that the channel creator/owner may leave
def test_leave_owner():

    # Check that user is actually part of the channel - if this fails, problem with dependencies
    assert(help.is_member(help.u_id))

    leave(help.token, help.channel_id)

    # Assert that user is no longer a member
    assert(not help.is_member(help.u_id))


# Check that a non-owner channel member may leave
def test_leave_member():

    # Invite a normal member to the channel
    ch.channel_invite(help.token, help.channel_id, help.u_id2)

    # Check that user is actually part of the channel - if this fails, problem with dependencies
    assert(help.is_member(help.u_id2))

    leave(help.token2, help.channel_id)

    # Assert that user is no longer a member
    assert(not help.is_member(help.u_id2))


# Test if AccessError exceptions are raised
# Should raise exception when:
#   User is not authorised (token invalid)
#   Authorised User is not a member of the channel_id (but channel_id exists)
def test_leave_access_error():
    assert(not help.is_member(help.u_id2))

    # User is not part of a channel, raise AccessError exception
    with pytest.raises(AccessError):
        leave(help.token2, help.channel_id)

    # User does not exist, raise AccessError
    with pytest.raises(AccessError):
        leave("INVALIDTOKEN", help.channel_id)


# Test if InputError's are raised
# Should raise when:
#   channel_id does not exist
def test_leave_input_error():

    # Channel does not exist, raise InputError
    with pytest.raises(InputError):
        leave(help.u_id, -100000)
