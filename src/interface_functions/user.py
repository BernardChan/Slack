# user/... functions for slackr app

from error import AccessError, InputError
from database_files.database_retrieval import get_users
from database_files.database_retrieval import get_users_by_key
from helper_functions.interface_function_helpers import is_valid_token
import database_files.database as db
import re


# USER/PROFILE
# Will use a GET request
# For a valid user, returns information about their user id, email, first name, last name, and handle
# Returns a profile dictionary
# Input Error for:
    # User with u_id is not a valid user
# Access Error for:
    # Token is not valid
def user_profile(token, u_id):

    # Raise an AccessError if not a valid token
    is_valid_token(token)
    
    # Go through all users and collect the correct user dictionary
    # If no users found with u_id, invalid u_id because user does not exist
    if get_users_by_key("u_id", u_id) == []:
        raise InputError(description="Invalid user id!")
    else:
        profile = get_users_by_key("u_id", u_id)[0]

    return profile

# USER/PROFILE/SETNAME
# Will use a PUT request
# Update the authorised user's first and last name, returns an empty dictionary
# Input Error for:
    # First or last name is not between 1 and 50 characters inclusive
# Access Error for:
    # Token is not valid
def user_profile_setname(token, name_first, name_last):
    
    # Raise an AccessError if not a valid token
    is_valid_token(token)

    # Raise an InputError if either name is out of bounds
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(description="First name is not between 1 and 50 characters!")
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(description="Last name is not between 1 and 50 characters!")
    
    # Get the user with the matching u_id by token
    match = get_users_by_key("token", token)
    u_id = match[0]["u_id"]
    # Update first and last name for the correct user
    for profile in db.DATABASE["users"]:
        if profile["u_id"] == u_id:
            profile["name_first"] = name_first
            profile["name_last"] = name_last
            break

    return {}

# USER/PROFILE/SETEMAIL
# Will use a PUT request
# Update the authorised user's email address, returns an empty dictionary
# Input Error for:
    # Email entered is not a valid email
    # Email address is being used by another user
# Acces Error for:
    # Invalid token
def user_profile_setemail(token, email):
    
    # Raise an AccessError if not a valid token
    is_valid_token(token)

    # Inner helper function for determining a valid email
    def valid_email(string):
        # Make a regular expression for validating email
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        # Pass the regular expression and the string using search() to check if valid
        if (re.search(regex, string)):
            return True
        else:
            return False
    # Raise an InputError if not a valid email
    if not valid_email(email):
        raise InputError(description="Invalid email!")

    # Raise an InputError if email is being used by another user
    # if get_users_by_key doesn't return an empty list (if users with profile["email"] = email are found)
    if get_users_by_key("email", email) != []:
        raise InputError(description="Email address in use by another user!")

    # Get the user with the matching u_id by token
    match = get_users_by_key("token", token)
    u_id = match[0]["u_id"]
    # Update email for the correct user
    for profile in db.DATABASE["users"]:
        if profile["u_id"] == u_id:
            profile["email"] = email
            break
    
    return {}

# USER/PROFILE/SETHANDLE
# Will use PUT request
# Update the authorised user's handle (display name), returns an empty dict
# Input Error for:
    # Handle not between 2 and 20 characters inclusive
    # Handle is in use by another user
# Access Error for:
    # Invalid token
def user_profile_sethandle(token, handle_str):
    
    # Raise an AccessError if not a valid token
    is_valid_token(token)

    # Raise an InputError if either name is out of bounds
    if len(handle_str) < 2 or len(handle_str) > 20:
        raise InputError(description="Handle (display name) is not between 2 and 20 characters!")

    # Raise an input error if handle is being used by another user
    # if get_users_by_key doesn't return an empty list (if users with profile["handle_str"] = handle are found)
    if get_users_by_key("handle_str", handle_str) != []:
        raise InputError(description="Handle (display name) in use by another user!")

    # Get the user with the matching u_id by token
    match = get_users_by_key("token", token)
    u_id = match[0]["u_id"]
    # Update handle for the correct user
    for profile in db.DATABASE["users"]:
        if profile["u_id"] == u_id:
            profile["handle_str"] = handle_str
            break

    return {}


# USERS/ALL
# Provides a list of all users and their respective details
# Only raises AccessError for invalid token
def users_all(token):

    # Raise an access error if not a valid token
    # TODO

    # Get the list of all users
    users = get_users()
    # return the list
    return { "users": users }
