# Tests for auth_register

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

# fixture is a good idea. So I call only one of the user profile ones 
# and go from there. 

"""
auth_register() elemental validation functions. 
# making sure each input to register() is valid
"""
#auth_register() Password Validation
def test_auth_register_short_password():
    with pytest.raises(InputError) as e:
        auth_register("bill.gates@microsoft.com", "123", "Bill", "Gates")

def test_auth_register_valid_password():
    auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates")


#auth_register() First Name Validation
def test_auth_register_invalid_first_name():
    with pytest.raises(InputError) as e:
        auth_register("bill.gates@microsoft.com", "123", "B"*51, "Gates")

def test_auth_register_valid_first_name():
    auth_register("bill.gates@microsoft.com", "123", "Bill", "Gates")


#auth_register() Last Name Validation
def test_auth_register_valid_last_name():
    auth_register("bill.gates@microsoft.com", "123", "Bill", "Gates")

def test_auth_register_invalid_last_name():
    with pytest.raises(InputError) as e:
        auth_register("bill.gates@microsoft.com", "123", "Bill", "G"*51)

#auth_register() Email Validation
def test__auth_register_valid_email():
    auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates")

def test_auth_register_invalid_email():
    with pytest.raises(InputError) as e:
        auth_register("bill.microsoft.com", "123456", "Bill", "Gates")

"""
register() interconnected validation functions
# making sure output behavior from register() is correct and valid
"""
    
# make sure register() returns a uID and token
def test_auth_register_duplicate_registration():
    register1 = auth_register("bill.gates@microsoft.com", "123", "Bill", "Gates")
 
    with pytest.raises(InputError) as e:
        #Email address is already being used by another user
        register2 = auth_register("bill.gates@microsoft.com", "123", "Bill", "Gates")
        assert (register1 != register2)
    
#python3 -m pytest auth_test.py
#command for if forgotten or lost
#test to see if my "git push -u origin auth" has worked 
#so I don't have to push it like this every single time
