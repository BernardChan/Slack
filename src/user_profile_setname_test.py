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
    
    # Call setname() to update first and last name of user
    user_profile_setname(ch.member_token, "Harry", "Potter")
    # Assert that this was successful
    assert_setname_success(ch.member_token, ch.member_id, "Harry", "Potter") 
    
    user_profile_setname(ch.member_token, "J. K.", "Simmons")
    assert_setname_success(ch.member_token, ch.member_id, "J. K.", "Simmons") 
    
    user_profile_setname(ch.member_token, "Red+Blue", "=Purple")
    assert_setname_success(ch.member_token, ch.member_id, "Red+Blue", "=Purple")

# Tests setname with numbers in name strings
def test_profile_setname_numbers():

    user_profile_setname(ch.member_token, "1234", "5678")
    assert_setname_success(ch.member_token, ch.member_id, "1234", "5678")
    
    user_profile_setname(ch.member_token, "JUL14N", "L33T")
    assert_setname_success(ch.member_token, ch.member_id, "JUL14N", "L33T")
    
    user_profile_setname(ch.member_token, "2+2", "=4")
    assert_setname_success(ch.member_token, ch.member_id, "2+2", "=4")
    
# Tests setname with special characters in name strings
def test_profile_setname_special_characters():

    user_profile_setname(ch.member_token, "\0", "\0")
    assert_setname_success(ch.member_token, ch.member_id, "\0", "\0")
    
    user_profile_setname(ch.member_token, "Harry\n", "Potter\t")
    assert_setname_success(ch.member_token, ch.member_id, "Harry\n", "Potter\t")
    
# Input error if first or last names aren't 0<x<51
def test_profile_setname_input_error():

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
        
# Access error if token passed is not a valid token
def test_profile_setname_access_error():

    # Raise error if user does not exist
    with pytest.raises(AccessError):
        user_profile_setname("INVALIDTOKEN", "Sigma", "Bolls")


   
    

        

