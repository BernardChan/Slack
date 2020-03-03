import pytest
from auth.py import login
from auth.py import logout
from auth.py import register
from error import InputError, AccessError

#Regular Expressions Module
import re

def test_register_short_password():
    with pytest.raises(InputError) as e:
        register("bill.gates@microsoft.com", "123", "Bill", "Gates")

def test_register_valid_name():
    register("bill.gates@microsoft.com", "123", "Bill", "Gates")

def test_register_valid_first_name():
    with pytest.raises(InputError) as e:
        register("bill.gates@microsoft.com", "123", "B"*51, "Gates")

def test_register_valid_first_name():
    with pytest.raises(InputError) as e:
        register("bill.gates@microsoft.com", "123", "Bill", "G"*51)
    
def test_email(email):
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):  
        #success needs do nothing right??
        pass
    else:  
        with pytest.raises(InputError) as e:
            
if __name__ == '__main__' :  
      
    # Enter the email  
    email = "bill.gates@microsoft.com"
      
    # calling run function  
    check(email) 
  
    email = "validemail@gmail.com"
    check(email) 
  
    email = "billyboi.com"
    check(email) 
