from channel import channel_addowner as add_owner

import pytest
import channel
from error import InputError, AccessError
import channel_helpers as ch


# Test that normal member can be added as owner to the public and private channel before being added to the channel
def test_addowner_member_before_add():

    # Set member as owner
    add_owner(ch.chan_owner_token, ch.channel_id, ch.member_id)
    add_owner(ch.chan_owner_token, ch.private_channel_id, ch.member_id)

    # Assert that member was set as an owner in both channels
    assert(ch.is_owner(ch.member_id, True))
    assert(ch.is_owner(ch.member_id, False))


# Test that normal member can be added as owner to the public and private channel after being added to the channels
def test_addowner_member_after_add():

    # Add member to channels
    channel.channel_invite(ch.chan_owner_token, ch.channel_id, ch.member_id)
    channel.channel_invite(ch.chan_owner_token, ch.private_channel_id, ch.member_id)

    # Set member as an owner
    add_owner(ch.chan_owner_token, ch.channel_id, ch.member_id)
    add_owner(ch.chan_owner_token, ch.private_channel_id, ch.member_id)

    # Assert that member was set as an owner in both channels
    assert(ch.is_owner(ch.member_id, True))
    assert(ch.is_owner(ch.member_id, False))


# Test that adding the slackr owner when they were not part the channel will not throw an error
#   Note: This is assuming that the user will also be added to the channel if they were not a part of the channel
def test_addowner_slackr_owner():
    add_owner(ch.chan_owner_token, ch.channel_id, ch.slackr_owner_id)
    add_owner(ch.chan_owner_token, ch.private_channel_id, ch.slackr_owner_id)

    # Assert that member was set as an owner in both channels
    assert(ch.is_owner(ch.slackr_owner_id, True))
    assert(ch.is_owner(ch.slackr_owner_id, False))


# Assert AccessError occurs when:
#   authorised user is not the channel owner or slackr owner
def test_addowner_access_error():

    # Authorised user is not channel owner and attempts to add another user
    with pytest.raises(AccessError):
        add_owner(ch.member_token, ch.channel_id, ch.member_id)


# Assert InputError occurs when
#   channel does not exist
#   when user is already owner of the channel
def test_addowner_input_error():

    # Channel does not exist, raise InputError
    with pytest.raises(InputError):
        add_owner(ch.chan_owner_token, -100000, ch.member_id)

    # User is already owner of channel
    with pytest.raises(InputError):
        add_owner(ch.chan_owner_token, ch.channel_id, ch.chan_owner_id)

    # Add slackr owner as a member of the channel (owner of the channel)
    channel.channel_invite(ch.chan_owner_token, ch.channel_id, ch.slackr_owner_id)
    channel.channel_invite(ch.chan_owner_token, ch.private_channel_id, ch.slackr_owner_id)

    # User is slackr owner and part of the channel
    with pytest.raises(InputError):
        add_owner(ch.chan_owner_token, ch.channel_id, ch.chan_owner_id)

