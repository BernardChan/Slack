# Tests for the leave() function in channel.py
# TODO: replace "VALIDTOKEN"s with an actual, valid token

import pytest
from channel import leave
from error import InputError, AccessError


# Test for a normal input
def test_leave_simple():
    pass


# Test if AccessError exceptions are raised
# Should raise exception when:
#   User is not authorised (token invalid)
#   Authorised User is not a member of the channel_id (but channel_id exists)
def test_leave_access_error():
    # TODO: give an invalid token as an arg
    # TODO: give an authorised user that isn't part of the channel

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


