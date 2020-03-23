import helper_functions.interface_function_helpers as help
from database_files.database import DATABASE as DATABASE

def channel_invite(token, channel_id):

    # include valid token function here, stub function atm
    def is_token_valid(token):
        pass
        
    # check if channel is valid
    help.check_channel_validity(channel_id)            
    # check if user is a member of the channel
    help.is_user_valid_channel_member(token, channel_id) 
    
    # check if user is valid
    help.is_valid_uid(u_id)
    
    # finds the user dictionary with user id and assigns it to user_invite
    for user in DATABASE["users"]:
        if user["u_id"] == u_id:
            user_invite = user
    
    # adds user to members list in channel 
    members = DATABASE['channels'][channel_id]['members']
    members.append(dict(user_invite))
    
    return {
    }
