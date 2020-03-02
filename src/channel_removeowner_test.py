# File for testing the channel_removeowner() function
# Dependencies on:
#   channel_addowner()
#   auth_register()
#   channel_details()
#   channel_invite()
#   channels_create()

# Test what happens when:
#   channel owner removes ownership over another member
#   channel owner removes ownership over the slackr owner
#   channel owner removes ownership over themselves
#   slackr owner removes ownership over another owner
#   slackr owner removes ownership over themselves

# Test that InputError occurs when:
#   channel_id does not exist
#   user_id is not an owner of the channel
#   user_id does not exist
#   user_id is not in the channel

# Test AccessError is thrown when:
#   Authorised user is not the owner of the channel

from channel import channel_removeowner as remove_owner
import pytest
import channel
import channel_helpers as ch
from error import InputError, AccessError


# TODO: go back through the other functions and check what happens when user is not authorised or they choose a
#   non-existent user as the target etc.
#   What happens if the channel ID doesn't exist?

# TODO: make sure you test for both public and private channels

# Test when channel owner removes another channel owner's ownership
def test_removeowner_simple():
    pass


# Test when slackr owner removes ownership on channel owner and themselves
def test_removeowner_slackr_owner():
    pass

# Test when channel owner removes ownership on slackr owner and themselves
def test_removeowner_channel_owner():
    pass


# Test input error when:
#   channel_id does not exist
#   user_id is not an owner of the channel
#   user_id does not exist
#   user_id is not in the channel
def test_removeowner_input_error():
    pass


# Test AccessError when:
#   Authorised user is not the owner of the channel
def test_removeowner_access_error():
    pass


