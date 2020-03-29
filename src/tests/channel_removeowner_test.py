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

from interface_functions.channel import channel_removeowner as remove_owner
import pytest
from interface_functions import channel
import helper_functions.test_helper_file as ch
from error import InputError, AccessError


# TODO: go back through the other functions and check what happens when user is not authorised or they choose a
#   non-existent user as the target etc.
#   What happens if the channel ID doesn't exist?

# TODO: make sure you test for both public and private channels
# TODO: refactor -100000 channel ID to be a variable

# Test when channel owner removes another channel owner's ownership
def test_removeowner_simple():

    # Set member as owner
    channel.channel_addowner(ch.chan_owner_token, ch.channel_id, ch.member_id)
    channel.channel_addowner(ch.chan_owner_token, ch.private_channel_id, ch.member_id)

    # Remove member's owner status
    remove_owner(ch.chan_owner_token, ch.channel_id, ch.member_id)
    remove_owner(ch.chan_owner_token, ch.private_channel_id, ch.member_id)

    assert(not ch.is_owner(ch.member_id, True))
    assert(not ch.is_owner(ch.member_id, False))


# Test when slackr owner removes ownership on channel owner and themselves
def test_removeowner_slackr_owner():
    if not ch.isFunctionImplemented(channel.channel_invite, -1, -1, -1):
        return

    # Add the slackr owner to the channel
    channel.channel_invite(ch.chan_owner_token, ch.channel_id, ch.slackr_owner_id)
    channel.channel_invite(ch.chan_owner_token, ch.private_channel_id, ch.slackr_owner_id)

    # Remove channel owner's owner status by the slackr owner
    remove_owner(ch.slackr_owner_token, ch.channel_id, ch.chan_owner_id)
    remove_owner(ch.slackr_owner_token, ch.private_channel_id, ch.chan_owner_id)

    # Remove slackr owner's owner status
    remove_owner(ch.slackr_owner_token, ch.channel_id, ch.slackr_owner_id)
    remove_owner(ch.slackr_owner_token, ch.private_channel_id, ch.slackr_owner_id)

    assert(not ch.is_owner(ch.chan_owner_id, True))
    assert(not ch.is_owner(ch.chan_owner_id, False))
    assert(not ch.is_owner(ch.slackr_owner_id, True))
    assert(not ch.is_owner(ch.slackr_owner_id, False))


# Test when channel owner removes ownership on slackr owner and themselves
def test_removeowner_channel_owner():
    if not ch.isFunctionImplemented(channel.channel_invite, -1, -1, -1):
        return

    # Add the slackr owner to the channel
    channel.channel_invite(ch.chan_owner_token, ch.channel_id, ch.slackr_owner_id)
    channel.channel_invite(ch.chan_owner_token, ch.private_channel_id, ch.slackr_owner_id)

    # Remove slackr owner's owner status
    remove_owner(ch.chan_owner_token, ch.channel_id, ch.slackr_owner_id)
    remove_owner(ch.chan_owner_token, ch.private_channel_id, ch.slackr_owner_id)

    # Remove channel owner's owner status
    remove_owner(ch.chan_owner_token, ch.channel_id, ch.chan_owner_id)
    remove_owner(ch.chan_owner_token, ch.private_channel_id, ch.chan_owner_id)

    assert(not ch.is_owner(ch.chan_owner_id, True))
    assert(not ch.is_owner(ch.chan_owner_id, False))


# Test input error when:
#   channel_id does not exist
#   user_id is not an owner of the channel
#   user_id does not exist
def test_removeowner_input_error():

    # Channel does not exist
    with pytest.raises(InputError):
        remove_owner(ch.chan_owner_token, ch.invalid_channel_id, ch.chan_owner_id)

    # user_id is not an owner of the channel
    with pytest.raises(InputError):
        remove_owner(ch.chan_owner_token, ch.channel_id, ch.member_id)

    # user_id does not exist
    with pytest.raises(InputError):
        remove_owner(ch.chan_owner_token, ch.channel_id, ch.invalid_user_id)


# Test AccessError when:
#   Authorised user is not the owner of the channel
def test_removeowner_access_error():

    # Authorised user is not an owner
    with pytest.raises(AccessError):
        remove_owner(ch.member_token, ch.channel_id, ch.member_id)
