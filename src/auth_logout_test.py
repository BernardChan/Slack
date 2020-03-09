import auth as a
import helper_functions.channel_helpers as ch

def test_logout():

    # check logout for each token
    assert a.auth_logout(ch.chan_owner_token) == True
    assert a.auth_logout(ch.slackr_owner_token) == True
    assert a.auth_logout(ch.member_token) == True
    
    # attempt to logout an invalid token
        
    # random string
    assert a.auth_logout("Token") == False
    
    # no input 
    assert a.auth_logout() == False
    

