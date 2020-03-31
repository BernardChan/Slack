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
