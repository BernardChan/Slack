import pytest
from auth import auth_login
from auth import auth_logout
from auth import auth_register
from error import InputError, AccessError

import sys
sys.path.append('../')

#Regular Expressions Module
#Used for email regular expressions
import re


"""
auth_register() validation function. 
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
def check_email(email):
    regex = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    if(re.search(regex,email)): 
        #success needs do nothing right??
        auth_register(email, "123456", "Bill", "Gates")
    else:  
        with pytest.raises(InputError) as e:
            auth_register(email, "123456", "Bill", "Gates")
       

def test_register_valid_email():
    email = "bill.gates@microsoft.com"
    check_email(email) 
  
def test_register_invalid_email():
    email = "billyboi.com"
    check_email(email) 
    
    
#python3 -m pytest auth_test.py
#command for if forgotten or lost    
