import database_files.database_retrieval as db
import helper_functions.interface_function_helpers as help
from database_files.database import DATABASE as DATABASE

def channel_join(token, channel_id):

    # include valid token function here, stub function atm
    def is_token_valid(token):
        pass
        
    # check if channel is valid
    help.check_channel_validity(channel_id)
            
    # check if user is a member of the channel
    help.is_user_valid_channel_member(token, channel_id) 
    member_join = db.get_users_by_key('token', token)
    
    # checks if authorized user is admin, if not channel is private
    help.is_slackr_admin(token)
    
    # adds user to members list in channel 
    members = DATABASE['channels'][channel_id]['members']
    members.append(dict(member_join))
    
    return {
    }
