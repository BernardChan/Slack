import auth
import channel_helpers as ch

def test_logout():
    # check logout for each token
    assert auth_logout(ch.chan_owner_token) == True
    assert auth_logout(ch.slackr_owner_token) == True
    assert auth_logout(ch.member_token) == True
    
    # attempt to logout an invalid token
    assert auth_logout(ch.token) == False
    assert auth_logout(Token) == False
    

