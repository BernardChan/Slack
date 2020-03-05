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
    
def test_profile_input_error(get_new_user):
    
    user_id, user_token = get_new_user
    
    user = user_profile(user_token, "INVALID_UID")
    
def test_profile_access_error(get_new_user):

    user_id, user_token = get_new_user
    
    user = user_profile("INVALIDTOKEN", user_id)        
    
