import pytest
from error import AccessError
#import helper_functions.test_helper_file as ch
from interface_functions.other import users_all
from interface_functions.auth import auth_register

"""
def test_users_all():
    assert users_all(ch.chan_owner_token) == [{ch.chan_owner_id, "email1@test.com", "first1", "last1", "handle1"}, {ch.slackr_owner_id, "email2@test.com", "first2", "last2", "handle2"}, {ch.member_id, "email3@test.com", "first3", "last3", "handle3"}]
    
    assert users_all(ch.slackr_owner_id) == [{ch.chan_owner_id, "email1@test.com", "first1", "last1", "handle1"},
    {ch.slackr_owner_id, "email2@test.com", "first2", "last2", "handle2"},
    {ch.member_id, "email3@test.com", "first3", "last3", "handle3"}]
    
    assert o.users_all(ch.user_id) == [{ch.chan_owner_id, "email1@test.com", "first1", "last1", "handle1"}, {ch.slackr_owner_id, "email2@test.com", "first2", "last2", "handle2"}, {ch.member_id, "email3@test.com", "first3", "last3", "handle3"}]
"""

def test_users_all_success_simple():
    # register 3 users
    bill_token = auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates")["token"]
    elon_token = auth_register("elon.musk@tesla.com", "123456", "Elon", "Musk")["token"]
    jeff_token = auth_register("jeff.bezos@amazon.com", "123456", "Jeff", "Bezos")["token"]
    
    
    users = users_all(bill_token)["users"]
    assert len(users) == 3
    assert users[0]["token"] == bill_token
    assert users[1]["token"] == elon_token
    assert users[2]["token"] == jeff_token
    assert users[0]["email"] == "bill.gates@microsoft.com"
    assert users[1]["email"] == "elon.musk@tesla.com"
    assert users[2]["email"] == "jeff.bezos@amazon.com"

def test_users_all_access_error():
    with pytest.raises(AccessError):
        users_all("INVALIDTOKEN")
