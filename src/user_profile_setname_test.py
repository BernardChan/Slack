# Tests for user_profile_setname() function in user.py
# Dependencies:
    # user_profile()

#NOTES
# A user is a dictionary containing 
# u_id, email, name_first, name_last, handle_str

import pytest
import channel_helpers as ch

from user import user_profile_setname
from user import user_profile

# Helper function to assert that setname was successful
def assert_setname_success(user_token, user_id, fname, lname):
    # Call the profile to be tested and assert that names are correct
    user = user_profile(user_token, user_id)
    assert(user["name_first"] == fname)
    assert(user["name_last"] == lname)

# Tests succesful setname
def test_profile_setname_success():
    
    # Calling setname
    user_profile_setname(ch.member_token, "Harry", "Potter")
    assert_setname_success(ch.member_token, ch.member_id, "Harry", "Potter")    

# Tests setname with numbers in name strings
def test_profile_setname_numbers():

    user_profile_setname(ch.member_token, "1234", "5678")
    assert_setname_success(ch.member_token, ch.member_id, "1234", "5678")
    
    user_profile_setname(ch.member_token, "JUL14N", "L33T")
    assert_setname_success(ch.member_token, ch.member_id, "JUL14N", "L33T")
    
# Input error if first or last names aren't 0<x<51
def test_profile_input_error():

    # Raise error if name is empty
    with pytest.raises(InputError) as e:
        user_profile_setname(ch.member_token, "", "Potter")

    with pytest.raises(InputError) as e:
        user_profile_setname(ch.member_token, "Harry", "")
    
    with pytest.raises(InputError) as e:
        user_profile_setname(ch.member_token, "", "")

    # Raise error if name > 50
    with pytest.raises(InputError) as e:
        user_profile_setname(ch.member_token,"a" * 51, "Potter")

    with pytest.raises(InputError) as e:
        user_profile_setname(ch.member_token, "Harry", "a" * 51)
    
    with pytest.raises(InputError) as e:
        user_profile_setname(ch.member_token, "a" * 51, "b" * 51)

   
    

        

