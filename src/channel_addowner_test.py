from channel import channel_addowner as add_owner


# TODO: Test that this function works when both owner/slackr owner add_owner

# Test that normal member can be added as owner to public and private channel
def test_addowner_member():

    # TODO: test when a member is and isn't already a part of the channel
    # TODO: for below 2 comments, add tests for public and private
    # Member is a part of the channel already


    # Member is not a part of the channel

    pass


# Test that adding the slackr owner when they were not part the channel will not throw an error
#   Note: This is assuming that the user will also be added to the channel if they were not a part of the channel
def test_addowner_slackr_owner():
    # TODO: private and public channels
    pass


# Assert AccessError occurs when:
#   authorised user is not the channel owner or slackr owner
def test_addowner_access_error():
    pass


# Assert InputError occurs when
#   channel does not exist
#   when user is already owner of the channel
# TODO: test adding slackr owner when already added
#   Test for channel owner
def test_addowner_input_error():
    pass

