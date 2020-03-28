# Tests for user_profile_setemail() function in user.py
# Dependencies:
    # workspace_reset()
    # user_profile()
    # auth_register()

import pytest

from interface_functions.auth import auth_register
from interface_functions.user import user_profile
from interface_functions.user import user_profile_setemail
from interface_functions.workspace_reset import workspace_reset
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

# Helper function to assert that setemail was successful
def assert_setemail_success(user_token, user_id, email):
    # Call the profile to be tested and assert that names are correct
    user = user_profile(user_token, user_id)
    assert(user["email"] == email)
    
# Tests successful profile setemail
def test_profile_setemail_success(user1):
    
    user_token, user_id = user1
    user_profile_setemail(user_token, "new.email@test.com")
    assert_setemail_success(user_token, user_id, "new.email@test.com")
    
    user_profile_setemail(user_token, "another.email@yay.org")
    assert_setemail_success(user_token, user_id, "another.email@yay.org")
    
    user_profile_setemail(user_token, "coolemail@notgmail.net")
    assert_setemail_success(user_token, user_id, "coolemail@notgmail.net")

    workspace_reset()
    
# Tests very similar emails
def test_profile_setemail_similar(user1, user2):
    
    token1, uid1 = user1
    token2, uid2 = user2
    
    user_profile_setemail(token1, "new.email@test.com")
    assert_setemail_success(token1, uid1, "new.email@test.com")
    # without "." delimiter - treated as different email
    user_profile_setemail(token2, "newemail@test.com")
    assert_setemail_success(token2, uid2, "newemail@test.com")

    workspace_reset()
    
# Invalid email (not following correct method) results in InputError
def test_profile_setemail_invalid(user1):

    user_token, user_id = user1
    with pytest.raises(InputError) as e:
        user_profile_setemail(user_token, "invalidemail.com")
        
    with pytest.raises(InputError) as e:
        user_profile_setemail(user_token, "invalidemail@no")
        
    with pytest.raises(InputError) as e:
        user_profile_setemail(user_token, "a.b.c@g.m")
        
    with pytest.raises(InputError) as e:
        user_profile_setemail(user_token, "hello!")

    workspace_reset()

# Input error if email address is being used by another user
def test_profile_setemail_duplicate_email(user1, user2):
    
    token1, uid1 = user1
    token2, uid2 = user2
    
    user_profile_setemail(token1, "test.user@test.com")
    user_profile_setemail(token2, "test2.user2@yay.com")

    # Member 1 tries to set email again to their current email
    with pytest.raises(InputError) as e:
        user_profile_setemail(token1, "test.user@test.com")
    
    # Member 1 tries to set email that is same as member2's
    with pytest.raises(InputError) as e:
        user_profile_setemail(token1, "test2.user2@yay.com")
        
    # Member 2 tries to set email that is same as member1's
    with pytest.raises(InputError) as e:
        user_profile_setemail(token2, "test.user@test.com")

    workspace_reset()

# Access error if token passed is invalid
def test_profile_setname_access_error():

    # Raise error if user does not exist
    with pytest.raises(AccessError) as e:
        user_profile_setemail("INVALIDTOKEN", "coolemail@test.com")

    workspace_reset()
