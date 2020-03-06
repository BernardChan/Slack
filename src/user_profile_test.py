# Tests for user_profile() function in user.py
# Dependencies:
    # auth_register()
    
import pytest

from auth import auth_register
from user import user_profile
from error import InputError

# Pytest fixture to regiser a new test user
@pytest.fixture
def get_new_user():
    data = auth_register("test.user@test.com", "password123", "fname", "lname")
    return data["u_id"], data["token"]

# Input error if invalid user id
def test_profile_input_error(get_new_user):
    
    user_id, user_token = get_new_user
    
    with pytest.raises(InputError) as e:
        user = user_profile(user_token, -100000)

# Access error if invalid token
def test_profile_access_error(get_new_user):

    user_id, user_token = get_new_user
    
    with pytest.raises(AccessError) as e:
        user = user_profile("INVALIDTOKEN", user_id)
        
# Both access and input error if invalid token and user id
def test_profile_input_and_access_error(get_new_user):
    user_id, user_token = get_new_user
    with pytest.raises( (AccessError, InputError) ):
         user = user_profile("INVALIDTOKEN", -100000)
    

