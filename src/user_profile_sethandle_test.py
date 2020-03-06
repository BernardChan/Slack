# Tests for user_profile_setname() function in user.py
# Dependencies:
    # user_profile()
    # auth_register()

import pytest

from auth import auth_register
from user import user_profile_sethandle
from user import user_profile
from error import InputError, AccessError

# Pytest fixture to register a new test user
@pytest.fixture
def get_new_user():
    data = auth_register("test.user@test.com", "password123", "fname", "lname")
    return data["u_id"], data["token"]

# Helper function to assert that sethandle was successful
def assert_sethandle_success(user_token, user_id, handle):
    # Call the profile to be tested and assert that handle is correct
    user = user_profile(user_token, user_id)
    assert(user["handle_str"] == handle)

# Test successful sethandle


# Input error when handle is not between 3 and 20 characters


# Input error when handle is in use by another user


# Access error when used with invalid token
