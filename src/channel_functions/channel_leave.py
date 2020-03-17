from error import AccessError, InputError
from database_files.database_retrieval import get_channels, is_user_in_channel
from database_files.database import DATABASE as DATABASE

def channel_leave(token, channel_id):

    # include valid token function here, stub function atm
    def is_token_valid(token):
        pass
        
    # check if channel is valid
    channels = get_channels()
    
    for channel in channels:
        if channel['channel_id'] == channel_id:
            pass
        else:
            raise InputError("The channel_id is not a valid channel")
            
    # check if user is a member of the channel
    if is_user_in_channel('token', token, channel_id) == False:
        raise AccessError("Authorised user is not a member of the channel")
        
    # remove the authorised user from the channel
    mem = DATABASE['channels'][channel_id]['members']
    for i in range(len(mem)):
        if chan[i]['token'] == token:
            del mem[i]
            break

    return {
    }
