import database_files.database_retrieval as db
import helper_functions.interface_function_helpers as help
from database_files.database import DATABASE as DATABASE

def channel_invite(token, channel_id, u_id):
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

def channel_details(token, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages(token, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

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

def channel_addowner(token, channel_id, u_id):
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

def channel_removeowner(token, channel_id, u_id):
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
            if user["permission_id"] == 2:
                raise InputError(f"User with user_id {u_id} is already the channel owner")
            else:
                user["permission_id"] = 2   

    return {
    }
