import helper_functions.system_test_helper_file as ch


def test_channel_addowner_simple():
    # Reset database and get relevant inputs
    # Create the user and owner of the channel, and the channel itself
    ch.reset()
    owner_u_id, owner_token = ch.get_channel_owner()
    user_u_id, user_token = ch.get_member()
    channel_id = ch.create_public_channel(owner_token)

    data = {
        "token": owner_token,
        "channel_id": channel_id,
        "u_id": user_u_id
    }
    print(f"data from test was {data}\n")
    print(f"ownerU_id={owner_u_id}, user_token = {user_token}")

    # Asert that the return value was correct and
    # that the member was added as a member and owner (under assumptions, this is the case)
    assert ch.make_post_request("channel/addowner", data) == {}
    assert ch.is_owner(user_token, channel_id)
