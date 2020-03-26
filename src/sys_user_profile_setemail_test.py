'''
System test for user/profile/setemail
Method: PUT
Input: (token, email)
Output: {}
'''

import helper_functions.system_test_helper_file as helper

def test_user_profile_setemail_simple():
    # reset database
    helper.reset()
    # make memeber and inputs dictionary
    u_id, token = helper.get_member()
    data = {
        "token": token,
        "email": "somenewemail@test.com"
    }
    # Assert returns correct output
    assert helper.make_put_request("user/profile/setemail", data) == {}
    # Check that email was changed
    user = helper.get_user_details(token, u_id)
    assert user["email"] == "somenewemail@test.com"
