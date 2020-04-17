import requests
import helper_functions.system_test_helper_file as ch

# Test is very basic since it only needs to test the HTTP request portion of
# the function, rather than their functionality (which is covered by integration tests)
# Test whether:
#   - Return value from channel/leave was correct
#   - User was correctly removed from the database

# =============================== README ===============================
# I'm making this file extra verbose to explain exactly what is happening
# Channel leave's specification looks like this:

# HTTP Route    | HTTP Method |     Parameter       |  Return Type
# channel/leave |     POST    | (token, channel_id) |      {}


# Check that the user left the channel
def test_channel_leave_simple():

    return  # Not implemented

    # Reset the database between tests so we don't have to restart the server
    ch.reset()

    # Calling the helper files to get the PARAMETERS needed for channel_leave(token, channel_id)
    token = ch.get_channel_owner()[1]
    channel_id = ch.create_public_channel(token)

    # PARAMETER for the function needs to be given as a dictionary
    data = {
        "token": token,
        "channel_id": channel_id
    }

    # 1. Choose the function based on the HTTP Method
    #       (channel_leave is POST, so we used make_post_request())
    # 2. Give the function your HTTP Route as a string
    #       (REMOVE the leading "/" if your route has it, e.g. /search becomes "search")
    #       (channel_leave uses channel/leave, so we give "channel/leave")
    # 3. Give it your data as a dictionary
    #       (channel_leave uses token, channel_id so I give {"token": ..., "channel_id":...}
    # 4. Assert that the HTTP METHOD (post) request returned the correct RETURN TYPE == {}
    assert ch.make_post_request("channel/leave", data) == {}

    # Check that the user was removed correctly
    # ========= IMPORTANT ==========
    # DO NOT ACCESS THE DATABASE DIRECTLY. Use/make helper functions that make requests for you
    # Accessing the database will NOT work.
    assert not ch.is_member(token, channel_id)


#################
# Channel Tests #
#################


def test_channel_join_simple():
    return  # this function isn't implemented yet

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


def test_channel_addowner_simple():
    # Reset database and get relevant inputs
    # Create the user and owner of the channel, and the channel itself
    ch.reset()
    owner_token = ch.get_channel_owner()[1]
    user_u_id, user_token = ch.get_member()
    channel_id = ch.create_public_channel(owner_token)

    data = {
        "token": owner_token,
        "channel_id": channel_id,
        "u_id": user_u_id
    }


    # Asert that the return value was correct and
    # that the member was added as a member and owner (under assumptions, this is the case)
    assert ch.make_post_request("channel/addowner", data) == {}

    assert ch.is_owner(user_token, channel_id)

def test_channel_removeowner_simple():
    # Reset database and get relevant inputs
    # Create the user and owner of the channel, and the channel itself
    ch.reset()
    owner_token = ch.get_channel_owner()[1]
    user_u_id, user_token = ch.get_member()
    channel_id = ch.create_public_channel(owner_token)

    data = {
        "token": owner_token,
        "channel_id": channel_id,
        "u_id": user_u_id
    }

    # Add a user as an owner, then remove them
    # Asert that the return value was correct
    ch.make_post_request("channel/addowner", data)
    assert ch.is_owner(user_token, channel_id)
    assert ch.make_post_request("channel/removeowner", data) == {}
    assert not ch.is_owner(user_token, channel_id)


##############
# User Tests #
##############


def test_user_profile_setemail_simple():
    # reset database
    ch.reset()
    # make memeber and inputs dictionary
    u_id, token = ch.get_member()
    data = {
        "token": token,
        "email": "somenewemail@test.com"
    }
    # Assert returns correct output
    assert ch.make_put_request("user/profile/setemail", data) == {}
    # Check that email was changed
    user = ch.get_user_details(token, u_id)["user"]
    assert user["email"] == "somenewemail@test.com"

def test_user_profile_sethandle_simple():
    # reset database
    ch.reset()
    # make member and inputs dictionary
    u_id, token = ch.get_member()
    data = {
        "token": token,
        "handle_str": "newhandle"
    }
    # assert returns correct output
    assert ch.make_put_request("user/profile/sethandle", data) == {}
    # check that handle was changed
    user = ch.get_user_details(token, u_id)["user"]
    assert user["handle_str"] == "newhandle"


def test_user_profile_setname_simple():
    # Reset
    ch.reset()
    # Make member
    u_id, token = ch.get_member()
    # Make input dict
    data = {
        "token": token,
        "name_first": "Harry",
        "name_last": "Potter"
    }
    # Assert returns correct output
    assert ch.make_put_request("user/profile/setname", data) == {}
    # Check that user's names were changed
    user = ch.get_user_details(token, u_id)["user"]
    assert user["name_first"] == "Harry"
    assert user["name_last"] == "Potter"


def test_user_profile_simple():
    # Reset database
    ch.reset()
    # get relevant inputs
    u_id, token = ch.get_member()
    data = {
        "token": token,
        "u_id": u_id
    }
    # Assert returns correct output (using user info from helper.get_member())
    assert ch.make_get_request("user/profile", data)["user"] == {
        "u_id": u_id,
        "email": "user@test.tst",
        "name_first": "user",
        "name_last": "member",
        "handle_str": "usermember",
        "profile_img_url": ""
    }



###################
# Other Functions #
###################

# Create a channel owner + channel
# Send a message to the channel
# Search for said messages and assert that they are found and returned
def test_search_simple():
    # Reset database and get relevant inputs
    ch.reset()
    token = ch.get_channel_owner()[1]
    channel_id = ch.create_public_channel(token)

    data = {
        "token": token,
        "query_str": "hello world"
    }

    ch.system_send_message(token, channel_id, "hello world")

    # Assert that the return value was correct
    message = ch.make_get_request("search", data)["messages"][0]
    assert message["message"] == "hello world"

# Reset the database
def test_reset():
    ch.make_post_request("workspace/reset", {})
    data = requests.get(f"http://127.0.0.1:42069/get/database")
    assert data.json() == {'users': [], 'messages': [], 'channels': []}
