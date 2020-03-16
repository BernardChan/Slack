# user/... functions for slackr app

from error import AccessError, InputError
from database_files.database_retrieval import get_users

# Helper function for checking if a token is valid or not
# Assumes that a token is the user's userid
def valid_token(token):
    # Go through all user ids and check if it exists
    users = get_users()
    for user in users:
        if user["u_id"] == token:
            return True
    return False

# USER/PROFILE
# For a valid user, returns information about their user id, email, first name, last name, and handle
# Input Error for:
    # User with u_id is not a valid user
# Access Error for:
    # Token is not valid
def user_profile(token, u_id):
    
    # Raise an AccessError if not a valid token
    if not valid_token(token):
        raise AccessError(description="Invalid token!")
    
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