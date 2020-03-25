import helper_functions.system_test_helper_file as ch


def test_channel_join_simple():
    # Reset database and get relevant inputs
    ch.reset()
    token = ch.get_channel_owner()[0]
    channel_id = ch.create_public_channel(token)

    data = {
        "token": token,
        "channel_id": channel_id
    }

    # Asert that the return value was correct and
    # that the user was added as a member
    assert ch.make_post_request("channel/join", data) == {}
    assert ch.is_member(token, channel_id)
