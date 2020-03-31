'''
System tests for user/profile/setname
Method: PUT
Input: (token, name_first, name_last)
Output: {}
'''

import helper_functions.system_test_helper_file as helper

def test_user_profile_setname_simple():
    # Reset
    helper.reset()
    # Make member
    u_id, token = helper.get_member()
    # Make input dict
    data = {
        "token": token,
        "name_first": "Harry",
        "name_last": "Potter"
    }
    # Assert returns correct output
    assert helper.make_put_request("user/profile/setname", data) == {}
    # Check that user's names were changed
    user = helper.get_user_details(token, u_id)
    assert user["name_first"] == "Harry"
    assert user["name_last"] == "Potter"
