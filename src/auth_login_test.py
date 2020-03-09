# Tests for auth_login

import pytest
from auth import auth_login
from auth import auth_logout
from auth import auth_register
from user import user_profile
from error import InputError, AccessError

import sys
sys.path.append('../')

# Dependancies:
    # user_profile()
    #auth_register()
    
# Assumptions
    # I can't test if a token is invalid in iteration 1 so I have to fudge it. 
    
# Tests
    # If token is valid
    # If token is invalid

def auth_login_valid_token():
    pass
    
def auth_login_invalid_token():
    
