from error import AccessError, InputError
from database_files.database_retrieval import get_users_by_key
from helper_functions.interface_function_helpers import is_valid_uid, is_slackr_admin, is_valid_token
import database_files.database as db

# ADMIN/USERPERMISSION/CHANGE
# Given a user by u_id, set their permissions to new permission_id
    # 1 = Owner, who can modify other owners' permissions
    # 2 = Members, who do not have any special permissions
# InputError for:
    # u_id does not refer to a valid user
    # permission_id does not refer to a value permission
# AccessError for:
    # Authorised user is not an admin or owner
    # Invalid token
def admin_userpermission_change(token, u_id, permission_id):

    # Access errors:
    # if invalid token
    is_valid_token(token)
    # if authorised user is not an admin or owner
    is_slackr_admin(token)

    # Input errors:
    # Check if u_id is valid
    is_valid_uid(u_id)
    # Check if permission_id is valid
    if (permission_id != 1 or permission_id != 2):
        raise InputError(description="Permission id does not refer to a value permission!")

    # Update permission id for the correct user
    for profile in db.DATABASE["users"]:
        if profile["u_id"] == u_id:
            profile["permission_id"] = permission_id
            break

    return {}