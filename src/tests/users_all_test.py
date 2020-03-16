from interface_functions import other as o
import helper_functions.test_helper_file as ch

def test_users_all():
    assert o.users_all(ch.chan_owner_token) == [{ch.chan_owner_id, "email1@test.com", "first1", "last1", "handle1"}, {ch.slackr_owner_id, "email2@test.com", "first2", "last2", "handle2"}, {ch.member_id, "email3@test.com", "first3", "last3", "handle3"}]
    
    assert o.users_all(ch.slackr_owner_id) == [{ch.chan_owner_id, "email1@test.com", "first1", "last1", "handle1"},
    {ch.slackr_owner_id, "email2@test.com", "first2", "last2", "handle2"},
    {ch.member_id, "email3@test.com", "first3", "last3", "handle3"}]
    
    assert o.users_all(ch.user_id) == [{ch.chan_owner_id, "email1@test.com", "first1", "last1", "handle1"}, {ch.slackr_owner_id, "email2@test.com", "first2", "last2", "handle2"}, {ch.member_id, "email3@test.com", "first3", "last3", "handle3"}]
    
