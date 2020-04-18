"""
 database_update.py
This file contains functions to change or add data to the database, so to avoid
directly accessing database at all times possible since implementation/structure
may change during the agile iteration process.
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
    """Generates a valid token based on the hash of input email"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    unique_combo = current_time + email
    token = hash_data(unique_combo)
    return token


"""
----------------------------------------------------------------------------------
Data Entry Functions
----------------------------------------------------------------------------------
"""
# Adding user.
def add_user_to_database(email, password, name_first, name_last, handle, u_id):
    """adds a user"""
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
    """returns a token and u_id given a token"""
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
    """Logs out user given a token"""
    is_success = False
    for user in db.DATABASE['users']:
        if user["token"] == token:
            user['token'] = ""
            is_success = True
    return is_success
