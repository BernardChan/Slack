'''
System test for user/profile/sethandle
Method: PUT
Input: (token, handle_str)
Output: {}
'''

import helper_functions.system_test_helper_file as helper

def test_user_profile_sethandle_simple():
    # reset database
    helper.reset()
    # make member and inputs dictionary
    u_id, token = helper.get_member()
    data = {
        "token": token,
        "handle_str": "newhandle"
    }
    # assert returns correct output
    assert helper.make_put_request("user/profile/sethandle", data) == {}
    # check that handle was changed
    user = helper.get_user_details(token, u_id)
    assert user["handle_str"] == "newhandle"
    