# Tests for user_profile_setname() function in user.py
# Dependencies:
    # auth_register()
    # user_profile()

#NOTES
# A user is a dictionary containing 
# u_id, email, name_first, name_last, handle_str

import pytest
import auth

from user import user_profile_setname
from user import user_profile

# Tests succesful setname
def test_profile_setname_success():
    
    # More test cases for successes needed?
    
    # Registering a test member
    member = auth_register("testmember@test.com", "password", "fname", "lname")
    member_token = member["token"]
    member_uid = member["u_id"]
    
    # Calling setname
    user_profile_setname(member_token, "Harry", "Potter")
    
    # Calling their profile and asserting that names updated
    user = user_profile(member_token, member_uid)
    assert(user["name_first"] == "Harry")
    assert(user["name_last"] == "Potter")
    
    
# Input error if first or last names aren't 0<x<51
def test_profile_setname_short_first_name():

    # Registering a test member
    member = auth_register("testmember@test.com", "password", "fname", "lname")
    member_token = member["token"]
    member_uid = member["u_id"]

    # Raise error if name is empty
    with pytest.raises(InputError) as e:
        user_profile_setname(member_token, "", "Potter")

    with pytest.raises(InputError) as e:
        user_profile_setname(member_token, "Harry", "")
    
    with pytest.raises(InputError) as e:
        user_profile_setname(member_token, "", "")

    # Raise error if name > 50
    with pytest.raises(InputError) as e:
        user_profile_setname(member_token,"a" * 51, "Potter")

    with pytest.raises(InputError) as e:
        user_profile_setname(member_token, "Harry", "a" * 51)
    
    with pytest.raises(InputError) as e:
        user_profile_setname(member_token, "a" * 51, "b" * 51)

   
    

        

