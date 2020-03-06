# Tests for user_profile_setname() function in user.py
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


# Input error when handle is not between 3 and 20 characters
def test_profile_set_handle(user1):

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
def test_profile_sethandle_duplicate_handle():

    member1 = auth_register("test.user@test.com", "password123", "fname", "lname")
    member2 = auth_register("test2.user2@yer.com", "123password", "Harry", "Potter")
    
    # Member 1 tries to set handle that is same as member2's
    with pytest.raises(InputError) as e:
        user_profile_sethandle(member1["token"], "harrypotter")
        
    # Member 2 tries to set handle that is same as member1's
    with pytest.raises(InputError) as e:
        user_profile_sethandle(member2["token"], "fnamelname")


# Access error when used with invalid token
