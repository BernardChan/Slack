import helper_functions.interface_function_helpers as help
from database_files.database import DATABASE as DATABASE

def channel_leave(token, channel_id):

    # include valid token function here, stub function atm
    def is_token_valid(token):
        pass
        
    # check if channel is valid
    help.check_channel_validity(channel_id)
            
    # check if user is a member of the channel
    help.is_user_valid_channel_member(token, channel_id)
        
    # remove the authorised user from the channel
    mem = DATABASE['channels'][channel_id]['members']
    for i in range(len(mem)):
        if mem[i]['token'] == token:
            del mem[i]
            break

    return {
    }
