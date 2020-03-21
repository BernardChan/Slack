from database_files.database_retrieval import get_users

# USERS/ALL
# Provides a list of all users and their respective details
# Only raises AccessError for invalid token
def users_all(token):

    # Raise an access error if not a valid token
    # TODO

    # Get the list of all users
    users = get_users
    # return the list
    return { "users": users }
