# Tests for the leave() function in channel.py
# Dependencies on:
#   auth_register()
#   channel_details()
#   channel_invite()

import pytest
import channels as chs
import channel as ch
from channel import channel_leave as leave
import auth
from error import InputError, AccessError


# Create a user that is part of a channel
login = auth.auth_register("test@test.tst", "password", "name", "lastname")
u_id = login["u_id"]
token = login["token"]

# Create a second user that is not part of the channel
login2 = auth.auth_register("test2@test.tst", "password2", "name2", "lastname2")
u_id2 = login2["u_id"]
token2 = login2["token"]

# Create public channel with user (token) in it
channel_id = chs.channels_create(token, "channel1", True)

# Get details of the channel
channel = ch.channel_details(token, channel_id)
channel_name = channel["name"]
channel_owner = channel["owner_members"]
channel_members = channel["all_members"]  # array of {u_id, name_first, name_last}


# Returns true if given user ID is part of the channel, else false
def is_member(user_id):
    return any([user_id == member["u_id"] for member in channel_members])


###############################
#            Tests            #
###############################

# Check that the channel creator/owner may leave
def test_leave_owner():

    # Check that user is actually part of the channel - if this fails, problem with dependencies
    assert(is_member(u_id))

    leave(token, channel_id)

    # Assert that user is no longer a member
    assert(not is_member(u_id))


# Check that a non-owner channel member may leave
def test_leave_member():

    # Invite a normal member to the channel
    ch.channel_invite(token, channel_id, u_id2)

    # Check that user is actually part of the channel - if this fails, problem with dependencies
    assert(is_member(u_id2))

    leave(token2, channel_id)

    # Assert that user is no longer a member
    assert(not is_member(u_id2))


# Test if AccessError exceptions are raised
# Should raise exception when:
#   User is not authorised (token invalid)
#   Authorised User is not a member of the channel_id (but channel_id exists)
def test_leave_access_error():
    assert(not is_member(u_id2))

    # User is not part of a channel, raise AccessError exception
    with pytest.raises(AccessError):
        leave(token2, channel_id)

    # User does not exist, raise AccessError
    with pytest.raises(AccessError):
        leave("INVALIDTOKEN", channel_id)


# Test if InputError's are raised
# Should raise when:
#   channel_id does not exist
def test_leave_input_error():

    # Channel does not exist, raise InputError
    with pytest.raises(InputError):
        leave(u_id, -100000)
