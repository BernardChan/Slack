from helper_functions.interface_function_helpers import is_valid_uid
from helper_functions.interface_function_helpers import is_slackr_admin
import database_files.database_retrieval as db

# Assumptions - if slackr owner removes themselves, there is no slackr owner anymore


# Takes u_id and removes them from the database (slackr)
def admin_user_remove(token, u_id):
    """
    Removes the user with the given u_id from the database

    :param token: The Owners of the Slackr with Admin Privileges
    :param u_id: User ID of the user to be removed
    :return: Returns an empty dictionary
    """

    # Input error when u_id is not found
    is_valid_uid(u_id)

    # Access Error if false
    is_slackr_admin(token)

    # Update permission id for the correct user
    user = db.get_users_by_key("u_id", u_id)[0]
    users = db.get_users()
    users.remove(user)

    return {}
