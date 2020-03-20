import database_files.database_retrieval as db
import helper_functions.interface_function_helpers as help
from database_files.database import DATABASE as DATABASE
from error import InputError

def channel_addowner(token, channel_id, u_id) 

    # include valid token function here, stub function atm
    def is_token_valid(token):
        pass
        
    # check if channel is valid
    help.check_channel_validity(channel_id)
    
    # check if user is a member of the channel
    help.is_user_valid_channel_member(token, channel_id) 
    
    
    # checks if authorized user is already an admin
    for user in DATABASE["users"]:  
        # find the right user    
        if user["u_id"] = u_id:
            if user["permission_id"] == 1:
                raise InputError(f"User with user_id {u_id} is already the channel owner")
            else:
                user["permission_id"] = 1   

    return {
    }
