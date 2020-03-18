# user/... functions for slackr app

from error import AccessError, InputError
from database_files.database_retrieval import get_users
from database_files.database_retrieval import get_users_by_key
import database_files.database as db

# USER/PROFILE
# For a valid user, returns information about their user id, email, first name, last name, and handle
# Returns a profile dictionary
# Input Error for:
    # User with u_id is not a valid user
# Access Error for:
    # Token is not valid
def user_profile(token, u_id):

    # Raise an AccessError if not a valid token
    #TODO
    
    # Go through all users and collect the correct user dictionary
    profile = {}
    users = get_users()
    for user in users:
        if user["u_id"] == u_id:
            profile = user

    # If profile is empty, u_id is invalid because user does not exist, so raise InputError
    if profile == {}:
        raise InputError(description="Invalid user id!")

    return profile

# USER/PROFILE/SETNAME
# Update the authorised user's first and last name
# Returns an empty dictionary
# Input Error for:
    # First or last name is not between 1 and 50 characters inclusive
# Access Error for:
    # Token is not valid
def user_profile_setname(token, name_first, name_last):
    
    # Raise an AccessError if not a valid token
    #TODO

    # Raise InputError if either name is out of bounds
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(description="First name is not between 1 and 50 characters!")
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(description="Last name is not between 1 and 50 characters!")
    
    # Get the user with the matching u_id to token
    #TODO:
    u_id = get_uid_by_token(token)

    # Update first and last name for the correct user
    # iterate through all profiles in database of users
    for profile in db.DATABASE["users"]:
        if profile["u_id"] == u_id:
            profile["name_first"] = name_first
            profile["name_last"] = name_last
            break

    return {}

def user_profile_setemail(token, email):
    return {
    }

def user_profile_sethandle(token, handle_str):
    return {
    }
