"""
File for functions that change or update the information in the Slackr database
"""

# pylint: disable=W0105 #pointless-string-statement
# pylint: disable=R0913 #too-many-arguments

from datetime import datetime
import database_files.database as db
from helper_functions.auth_helper import hash_data

"""
----------------------------------------------------------------------------------
Token Functions
----------------------------------------------------------------------------------
"""
def get_valid_token(email):
    """
    Generates a valid token based on the hash of input email
    :param email: inputted email of the user
    :return: returns token
    """    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    unique_combo = current_time + email
    token = hash_data(unique_combo)
    return token


"""
----------------------------------------------------------------------------------
Data Entry Functions
----------------------------------------------------------------------------------
"""
def add_user_to_database(email, password, name_first, name_last, handle, u_id):
    """adds a user"""
    """
    Adds a user to the database
    :param email: inputted email of the user
    :param password: user's inputted password
    :param name_first: the user's given name
    :param name_last: the user's family name
    :param handle: the user's Slackr handle
    :param u_id: the user's unique identifier for their record in the database
    :return: returns dictonary containing u_id and token
    """
    permission_id = 0
    if not db.DATABASE["users"]:
        permission_id = 1
    else:
        permission_id = 2

    token = get_valid_token(email)

    new_user = {
        "u_id": u_id,
        "email": email,
        "password": password,
        "name_first": name_first,
        "name_last": name_last,
        "handle_str": handle,
        "token": token,
        "permission_id": permission_id,
        "profile_img_url": "",
        "reset_code": None
    }

    db.DATABASE['users'].append(new_user)

    register_dict = {
        'u_id' : u_id,
        'token' : token
    }
    return register_dict


def login_user(email):
    """
    Records the user log in token in the database and returns the u_id and token
    :param email: inputted email of the user
    :return: returns dictionary containing u_id and token
    """
    for user in db.DATABASE['users']:
        if user["email"] == email:
            token = get_valid_token(email)
            user['token'] = token
            u_id = user['u_id']

    return {
        'u_id': u_id,
        'token': token,
    }


def logout_user(token):
    """
    Erases the user log in token in the database and returns boolean is_success
    :param token: the user's current login token
    :return: returns boolean is_success
    """
    is_success = False
    for user in db.DATABASE['users']:
        if user["token"] == token:
            user['token'] = ""
            is_success = True
    return is_success
