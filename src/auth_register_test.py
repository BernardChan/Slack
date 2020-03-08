# Tests for auth_register

# Dependancies:
    # user_profile()
    #auth_register()
    #auth_login()
    #auth_logout()
    
# Assumptions 
    # Special characters are permitted for first/last names
    # Registration gives a session so it must log you in when you register
    
# Test what happens when:
# Testing of individual elements
    # password is entered correctly
    # password is below minimum characters
    # first name entered correctly
    # first name entered with too many characters
    # first name entered incorrectly (as integer)
    # last name entered correctly (as string)
    # last name entered with too many characters
    # email entered correctly
    # email entered incorrectly
# Test for:
# Testing of interconnected elements
    # that register returns a uid and token
    # duplicate registration requests
    #

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
register0 = auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates")

"""
auth_register() elemental validation functions. 
# making sure each input to register() is valid
"""
#auth_register() Password Validation
def test_auth_register_short_password():
    with pytest.raises(InputError) as e:
        auth_register("bill.gates@microsoft.com", "123", "Bill", "Gates")

def test_auth_register_valid_password():
    assert auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates")


#auth_register() First Name Validation
def test_auth_register_invalid_first_name():
    with pytest.raises(InputError) as e:
        auth_register("bill.gates@microsoft.com", "123", "B"*51, "Gates")

def test_auth_register_valid_first_name():
    assert auth_register("bill.gates@microsoft.com", "123", "Bill", "Gates")
    
def test_auth_register_integer_first_name():
    passwordInteger = 123456
    if not isinstance(passwordInteger, str):
        with pytest.raises(InputError) as e:
            auth_register("bill.gates@microsoft.com", 123456, "Bill", "Gates")
            
def test_auth_register_string_first_name():
    passwordString = "123456"
    if not isinstance(passwordString, str):
        assert auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates")
            
#auth_register() Last Name Validation
def test_auth_register_valid_last_name():
    assert auth_register("bill.gates@microsoft.com", "123", "Bill", "Gates")

def test_auth_register_invalid_last_name():
    with pytest.raises(InputError) as e:
        auth_register("bill.gates@microsoft.com", "123", "Bill", "G"*51)

#auth_register() Email Validation
def test__auth_register_valid_email():
    assert auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates")

def test_auth_register_invalid_email():
    with pytest.raises(InputError) as e:
        auth_register("bill.microsoft.com", "123456", "Bill", "Gates")

"""
register() interconnected validation functions
# making sure output behavior from register() is correct and valid
"""
    
# make sure register() returns a uID and token
def test_auth_register_return():
    register1 = auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates")
 
# test for duplicate registration attempts with the same user_profile
def test_auth_register_duplicate_registration():
    register1 = auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates")
 
    with pytest.raises(InputError) as e:
        #Email address is already being used by another user
        register2 = auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates")
        # assert (register1 != register2)
    
#python3 -m pytest auth_register_test.py
#command for if forgotten or lost
#test to see if my "git push -u origin auth" has worked 
#so I don't have to push it like this every single time
