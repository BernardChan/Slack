"""
 auth.py
This function takes in input from the user, validates it,checks against
the database, then authenticates them if everything is correct.
"""
#pylint: disable=W0105

# Usage
    # Used for Validation of input only.

# Additions:
# 21/03/20
    # - register finished
# 23/03/20
    # - Login and Logout

from error import InputError
import database_files.database_update as du
import database_files.database_retrieval as dr
import helper_functions.auth_helper as ah
import helper_functions.interface_function_helpers as helper

"""
----------------------------------------------------------------------------------
User Interface Functions
----------------------------------------------------------------------------------
"""
def auth_register(email, password, name_first, name_last):
    """Registers user in database"""
    # Stage 1 - Validate input.
    ah.validate_email(email)
    ah.validate_password(password)
    ah.validate_name_first(name_first)
    ah.validate_name_last(name_last)

    # Stage 2 - check database
    if dr.is_duplicate("email", email):
        raise InputError(description='Email address is already being used by another user')

    # Stage 4 - Store all user information in the database
    u_id_returned = helper.get_unique_id()
    register_dict = du.add_user_to_database(email, ah.hash_data(password),\
        name_first, name_last, ah.create_handle(name_first, name_last), \
        u_id_returned \
    )
    return register_dict

def auth_login(email, password):
    """Logs in user if they are already registered"""
    # Validate Email
    ah.validate_email(email)
    user_rec = dr.get_users_by_key("email", email)
    if user_rec == []:
        raise InputError(description='Login attempt not successsful')

    # Validate Password
    hash_pw = ah.hash_data(password)
    if hash_pw != user_rec[0]["password"]:
        raise InputError(description='Password is not correct')

    # Create and assign token to database
    # new_token = ah.get_valid_token(email)
    login_dict = du.login_user(email)

    return login_dict


def auth_logout(token):
    """logs out a user if they were registered and currently logged in"""
    is_success = du.logout_user(token)
    return {"is_success": is_success}
