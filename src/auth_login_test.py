# Tests for auth_login

# Dependancies:
    # user_profile()
    #auth_register()

import pytest
from auth import auth_login
from auth import auth_logout
from auth import auth_register
from user import user_profile
from error import InputError, AccessError

import sys
sys.path.append('../')

# Tests to run
    # register then login success
    # Rego not the same as login
    # Login with wrong password error
    # login with duplicate uid
    # Register and login with two different requests and assert u_id is different
    # Register and login with two users but with token not the u_id. 
    
def test_auth_login_register_then_login_success():
    register1 = auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates")
    login1 = auth_login("bill.gates@microsoft.com", "123456")
    assert register1['u_id'] == login1['u_id']
    
def test_auth_login_no_user_found():
    register1 = auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates")
    with pytest.raises(InputError) as e:
        login1 = auth_login("bill.gates@microsoft.co", "123456")
        
def test_auth_login_wrong_password():
    register1 = auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates")
    with pytest.raises(InputError) as e:
        login1 = auth_login("bill.gates@microsoft.com", "wrong_password")

def test_auth_login_invalid_email_format():
    register1 = auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates")
    with pytest.raises(InputError) as e:
        login1 = auth_login("bill.gatemicrosoft.com", "123456")

def test_auth_login_different_ids():
    register1 = auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates")
    login1 = auth_login("bill.gates@microsoft.com", "123456")
    register2 = auth_register("andy.gates@microsoft.com", "24681012", "Andy", "Gates")
    login2 = auth_login("andy.gates@microsoft.com", "24681012")
    with pytest.raises(InputError) as e:
        assert login2['u_id'] != login1['u_id']
        # currently fails as stub provides same u_id, but will work later
        
def test_auth_login_different_tokens():
    register1 = auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates")
    login1 = auth_login("bill.gates@microsoft.com", "123456")
    register2 = auth_register("andy.gates@microsoft.com", "24681012", "Andy", "Gates")
    login2 = auth_login("andy.gates@microsoft.com", "24681012")
    with pytest.raises(InputError) as e:
        assert login1['token'] != login2['token']
        # currently fails as stub provides same token, but will work later

# python3 -m pytest auth_login_test.py
