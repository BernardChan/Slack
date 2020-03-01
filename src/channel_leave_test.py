# Tests for the leave() function in channel.py
# TODO: need to make sure passwords, names etc. for auth_register are valid and will not return an error

import pytest
import channels as chs
import channel as ch
import auth
from error import InputError, AccessError


# Setting global variables
login = auth.auth_register("test@test.tst", "password", "name", "lastname")
u_id = login["u_id"]
token = login["token"]

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


# Test for a normal input
def test_leave_simple():

    # Check that user is actually part of the channel - if this fails, problem with dependencies
    assert(is_member(u_id))

    ch.channel_leave(token, channel_id)

    # Assert that user is no longer a member
    assert(not is_member(u_id))


# Test if AccessError exceptions are raised
# Should raise exception when:
#   User is not authorised (token invalid)
#   Authorised User is not a member of the channel_id (but channel_id exists)
def test_leave_access_error():
    # TODO: give an invalid token as an arg
    # TODO: give an authorised user that isn't part of the channel

    # Create a second user that is not part of the channel
    login2 = auth.auth_register("test2@test.tst", "password2", "name2", "lastname2")
    u_id2 = login["u_id"]
    token2 = login["token"]

    pass


# Test if InputError's are raised
# Should raise when:
#   channel_id does not exist
def test_leave_input_error():
    pass
    # Dependent on channels.list(token)? How do we know if a channel is valid or not
    # assuming that leave() calls channels_listall()
    #
    # with pytest.raises(InputError):
    #     leave("VALIDTOKEN", -10)


