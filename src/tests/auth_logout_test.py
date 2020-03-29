# Tests for auth_logout

# Dependancies:
    # user_profile()
    #auth_register()
    # auth_login()

import pytest
from interface_functions.auth import auth_login
from interface_functions.auth import auth_logout
from interface_functions.auth import auth_register
from error import InputError
from interface_functions.workspace_reset import workspace_reset

import sys
sys.path.append('../')

# Tests to run
    # register then login then logout success
    # logout with no valid token found
    # login with two tokens simultaniously
    
def test_auth_login_register_then_login_success():
    workspace_reset()
    register1 = auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates")
    login1 = auth_login("bill.gates@microsoft.com", "123456")
    logout1 = auth_logout(login1["token"])
    print(f"logout1 was {logout1}")
    assert logout1["is_success"] == True
        
def test_auth_login_different_tokens():
    workspace_reset()
    register1 = auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates")
    login1 = auth_login("bill.gates@microsoft.com", "123456")
    register2 = auth_register("andy.gates@microsoft.com", "24681012", "Andy", "Gates")
    login2 = auth_login("andy.gates@microsoft.com", "24681012")
    logout1 = auth_logout(login1["token"]) 
    logout2 = auth_logout(login2["token"]) 
    assert logout1 == logout2

# python3 -m pytest auth_logout _test.py
