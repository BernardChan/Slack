import helper_functions.system_test_helper_file as ch


# Create a channel owner + channel
# Send a message to the channel
# Search for said messages and assert that they are found and returned
def test_search_simple():
    # Reset database and get relevant inputs
    ch.reset()
    u_id, token = ch.get_channel_owner()
    channel_id = ch.create_public_channel(token)

    data = {
        "token": token,
        "query_str": "hello world"
    }

    ch.system_send_message(token, channel_id, "hello world")

    # Assert that the return value was correct
    message = ch.make_get_request("search", data)["messages"][0]
    assert message["message"] == "hello world"
