# Tests for channel_addowner() function
# Dependencies:
#   auth_register()
#   channel_details()
#   channel_invite()
#   channels_create()

from channel import channel_addowner as add_owner
import pytest
import channel
from helper_functions.helpers import public_channel, private_channel
from helper_functions.helpers import member, channel_owner, is_owner, slackr_owner
from error import InputError, AccessError


# Test that normal member can be added as owner to the public and private channel before being added to the channel
def test_addowner_member_before_add(member, channel_owner, public_channel, private_channel, is_owner):
    member_id           = member[0]
    chan_owner_token    = channel_owner[1]
    public_id           = public_channel[1]
    private_id          = private_channel[1]

    # Set member as owner
    add_owner(chan_owner_token, public_id, member_id)
    add_owner(chan_owner_token, private_id, member_id)

    # Assert that member was set as an owner in both channels
    assert(is_owner(member_id, True))
    assert(is_owner(member_id, False))


# Test that normal member can be added as owner to the public and private channel after being added to the channels
def test_addowner_member_after_add(member, channel_owner, public_channel, private_channel, is_owner):
    member_id           = member[0]
    chan_owner_token    = channel_owner[1]
    public_id           = public_channel[1]
    private_id          = private_channel[1]

    # Add member to channels
    channel.channel_invite(chan_owner_token, public_id, member_id)
    channel.channel_invite(chan_owner_token, private_id, member_id)

    # Set member as an owner
    add_owner(chan_owner_token, public_id, member_id)
    add_owner(chan_owner_token, private_id, member_id)

    # Assert that member was set as an owner in both channels
    assert(is_owner(member_id, True))
    assert(is_owner(member_id, False))


# Test that adding the slackr owner when they were not part the channel will not throw an error
#   Note: This is assuming that the user will also be added to the channel if they were not a part of the channel
def test_addowner_slackr_owner(channel_owner, public_channel, private_channel, is_owner, slackr_owner):
    chan_owner_token    = channel_owner[1]
    public_id           = public_channel[1]
    private_id          = private_channel[1]
    slackr_owner_id     = slackr_owner[0]

    add_owner(chan_owner_token, public_id, slackr_owner_id)
    add_owner(chan_owner_token, private_id, slackr_owner_id)

    # Assert that member was set as an owner in both channels
    assert(is_owner(slackr_owner_id, True))
    assert(is_owner(slackr_owner_id, False))


# Assert AccessError occurs when:
#   authorised user is not the channel owner or slackr owner
def test_addowner_access_error(member, public_channel):
    member_id, member_token = member
    public_id = public_channel[1]

    # Authorised user is not channel owner and attempts to add another user
    with pytest.raises(AccessError):
        add_owner(member_token, public_id, member_id)


# Assert InputError occurs when
#   channel does not exist
#   when user is already owner of the channel
def test_addowner_input_error(member, channel_owner, public_channel, private_channel, slackr_owner):

    # Channel does not exist, raise InputError
    with pytest.raises(InputError):
        add_owner(channel_owner[1], -100000, member[0])

    # User is already owner of channel
    with pytest.raises(InputError):
        add_owner(channel_owner[1], public_channel[1], channel_owner[0])

    # Add slackr owner as a member of the channel (owner of the channel)
    channel.channel_invite(channel_owner[1], public_channel[1], slackr_owner[0])
    channel.channel_invite(channel_owner[1], private_channel[1], slackr_owner[0])

    # User is slackr owner and part of the channel
    with pytest.raises(InputError):
        add_owner(channel_owner[1], public_channel[1], channel_owner[0])

