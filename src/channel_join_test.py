# Tests for the channel_join() function in channel.py
# TODO: assert before/after function to check if user successfully did not exist/did join

import pytest
import channels as chs
import channel as ch
from channel import channel_leave as leave
import auth
from error import InputError, AccessError
import channel_helpers


# Check that a normal user can join a public channel
def test_join_normal():
    pass


# Check that admin can join a public channel (slakr owner)
def test_join_admin_public():
    pass


# Check that admin can join a private channel (slakr owner)
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
