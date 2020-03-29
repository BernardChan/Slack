# Tests for auth_register

# Dependencies:
    # workspace_reset()
    # auth_register()
    
# Assumptions 
    # Special characters are permitted for first/last names
    # Registration gives a session so it must log you in when you register
    
# Test what happens when:
# Testing of individual elements
    # password is entered correctly
    # password is below minimum characters
    # password entered with empty value
    # first name entered correctly
    # first name entered with too many characters
    # first name entered with empty value
    # last name entered correctly
    # last name entered with too many characters
    # last name entered with empty value
    # email entered correctly
    # email entered incorrectly
# Test for:
# Testing of interconnected elements
    # that register returns a uid and token
    # duplicate registration requests
    #

import sys
sys.path.append('../')

import pytest
from interface_functions.auth import auth_register
from error import InputError

from interface_functions.workspace_reset import workspace_reset
from helper_functions.interface_function_helpers import is_valid_token
from helper_functions.interface_function_helpers import is_valid_uid

"""
----------------------------------------------------------------------------------
auth_register() elemental validation functions. 
----------------------------------------------------------------------------------
"""     
#auth_register() Password Validation
def test_auth_register_short_password():
    workspace_reset()
    with pytest.raises(InputError) as e:
        auth_register("bill.gates@microsoft.com", "123", "Bill", "Gates")

def test_auth_register_no_password():
    workspace_reset()
    with pytest.raises(InputError):
        auth_register("bill.gates@microsoft.com","", "Bill", "Gates")

#auth_register() First Name Validation
def test_auth_register_long_first_name():
    workspace_reset()
    with pytest.raises(InputError) as e:
        auth_register("bill.gates@microsoft.com", "123456", "B"*51, "Gates")

def test_auth_register_no_first_name():
    workspace_reset()
    with pytest.raises(InputError) as e:
        auth_register("bill.gates@microsoft.com", "123456","", "Gates")
        

#auth_register() Last Name Validation
def test_auth_register_long_last_name():
    workspace_reset()
    with pytest.raises(InputError) as e:
        auth_register("bill.gates@microsoft.com", "123456", "Bill", "G"*51)

def test_auth_register_no_last_name():
    workspace_reset()
    with pytest.raises(InputError) as e:
        auth_register("bill.gates@microsoft.com", "123456","Bill", "")
        

#auth_register() Email Validation
def test_auth_register_no_email():
    workspace_reset()
    with pytest.raises(InputError) as e:
        auth_register("", "123456", "Bill", "Gates")

def test_auth_register_invalid_email_missing_at_symbol():
    workspace_reset()
    with pytest.raises(InputError) as e:
        auth_register("bill.gatesmicrosoft.com", "123456", "Bill", "Gates")
        
def test_auth_register_invalid_email_no_top_level_domain():
    workspace_reset()
    with pytest.raises(InputError) as e:
        auth_register("bill.gates@microsoft", "123456", "Bill", "Gates")
        
def test_auth_register_invalid_email_misspelt_top_level_domain():
    workspace_reset()
    with pytest.raises(InputError) as e:
        auth_register("bill.gates@microsoft.comk", "123456", "Bill", "Gates")

def test_auth_register_invalid_email_missing_local_segment():
    workspace_reset()
    with pytest.raises(InputError) as e:
        auth_register("@microsoft.com", "123456", "Bill", "Gates")


"""
------------------------------------------------------------------------------------------
register() interconnected validation functions
------------------------------------------------------------------------------------------
"""     
# make sure register() returns a uID and token
def test_auth_register_return():
    workspace_reset()
    register1 = auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates")
    assert is_valid_uid(reg1['u_id'])
    assert is_valid_token(reg1['token'])
    # Function 2 D
 
# test for duplicate registration attempts with the same user_profile
def test_auth_register_duplicate_registration():
    workspace_reset()
    register1 = auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates") 
    with pytest.raises(InputError) as e:
        register2 = auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates")
    
#python3 -m pytest auth_register_test.py
#command for if forgotten or lost
#test to see if my "git push -u origin auth" has worked 
#so I don't have to push it like this every single time
