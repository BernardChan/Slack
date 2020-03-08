# Tests for user_profile_sethandle() function in user.py
# Dependencies:
    # user_profile()
    # auth_register()

import pytest

from auth import auth_register
from user import user_profile_sethandle
from user import user_profile
from error import InputError, AccessError

# Pytest fixture to regiser test user 1
@pytest.fixture
def user1():
    data = auth_register("test.user1@test.com", "password123", "fname1", "lname1")
    return data["token"], data["u_id"]
    
# Pytest fixture to regiser test user 2
@pytest.fixture
def user2():
    data = auth_register("test.user2@test.com", "123password", "fname2", "lname2")
    return data["token"], data["u_id"]


# Helper function to assert that sethandle was successful
def assert_sethandle_success(user_token, user_id, handle):
    # Call the profile to be tested and assert that handle is correct
    user = user_profile(user_token, user_id)
    assert(user["handle_str"] == handle)

# Test successful sethandle
def test_profile_sethandle_success(user1):

    user_token, user_id = user1
    user_profile_sethandle(user_token, "newhandle")
    assert_sethandle_success(user_token, user_id, "newhandle")
    
    user_profile_sethandle(user_token, "cool.handle18")
    assert_sethandle_success(user_token, user_id, "cool.handle18")
    
    user_profile_sethandle(user_token, "red+blue=purple")
    assert_sethandle_success(user_token, user_id, "red+blue=purple")
    
# Tests sethandle with special characters
def test_profile_sethandle_special_characters(user1):

    user_token, user_id = user1
    user_profile_sethandle(user_token, "Hey\n")
    assert_sethandle_success(user_token, user_id, "Hey\n")
    
    user_profile_sethandle(user_token, "Hi!\t")
    assert_sethandle_success(user_token, user_id, "Hi!\t")
    

# Input error when handle is not between 3 and 20 characters
def test_profile_sethandle_input_error(user1):

    user_token, user_id = user1
    with pytest.raises(InputError) as e:
        user_profile_sethandle(user_token, "")
        
    with pytest.raises(InputError) as e:
        user_profile_sethandle(user_token, "12")
        
    with pytest.raises(InputError) as e:
        user_profile_sethandle(user_token, "a" * 21)
        
    with pytest.raises(InputError) as e:
        user_profile_sethandle(user_token, "a" * 50)

# Input error when handle is in use by another user
def test_profile_sethandle_duplicate_handle(user1, user2):

    token1, uid1 = user1
    token2, uid2 = user2

    user_profile_sethandle(token1, "1CoolHandle")
    user_profile_sethandle(token2, "2BetterHandle")
    
    # Member 1 tries to set handle that is same as member2's
    with pytest.raises(InputError) as e:
        user_profile_sethandle(token1, "2BetterHandle")
        
    # Member 2 tries to set handle that is same as member1's
    with pytest.raises(InputError) as e:
        user_profile_sethandle(token2, "1CoolHandle")


# Access error when used with invalid token
def test_profile_sethandle_access_error():

    # Raise error if invalid token
    with pytest.raises(AccessError) as e:
        user_profile_sethandle("INVALIDTOKEN", "newhandle")
