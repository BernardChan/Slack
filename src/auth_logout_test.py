import auth
import helper_functions.channel_helpers as ch

def test_logout():
    # check logout for each token
    assert auth_logout(ch.chan_owner_token) == True
    assert auth_logout(ch.slackr_owner_token) == True
    assert auth_logout(ch.member_token) == True
    
    # attempt to logout an invalid token
    
    # token not in helper function
    assert auth_logout(ch.token) == False
    
    # random string
    assert auth_logout(Token) == False
    
    # no input 
    assert auth_logout() == False
    

