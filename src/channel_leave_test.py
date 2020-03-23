import helper_functions.system_test_helper_file as ch
import database_files.database_retrieval as db

# Test is very basic since it only needs to test the HTTP request portion of
# the function, rather than their functionality (which is covered by integration tests)
# Test whether:
#   - Return value from channel/leave was correct
#   - User was correctly removed from the database


# Check that the user actually left the channel
def test_channel_leave_simple():
    ch.reset()
    u_id, token = ch.get_channel_owner()
    channel_id = ch.create_public_channel(token)

    data = {
        "token": token,
        "channel_id": channel_id
    }

    assert ch.make_post_request("channel/leave", data) == {}
    assert not db.is_user_in_channel("token", token, channel_id)
