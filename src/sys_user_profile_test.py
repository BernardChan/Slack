'''
System tests for user/profile
Method: GET
Input: (token, u_id)
Output: { user }
    user dictionary: u_id, email, name_first, name_last, handle_str
'''


import helper_functions.system_test_helper_file as helper

def test_user_profile_simple():
    # Reset database
    helper.reset()
    # get relevant inputs
    u_id, token = helper.get_member()
    data = {
        "token": token,
        "u_id": u_id
    }
    # Assert returns correct output (using user info from helper.get_member())
    assert helper.make_get_request("user/profile", data) == {
        "u_id": u_id,
        "email": "user@test.tst",
        "name_first": "user",
        "name_last": "member",
        "handle_str": "usermember"
    }
    