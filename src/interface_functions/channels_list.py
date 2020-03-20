from database_files.database_retrieval import get_user_channels_by_key

# CHANNELS/LIST
# Provides a list of all channels (and their associated etails) that the user is part of
# Only raises AccessError for invalid token
def channels_list(token):

    # Raise an access error if not a valid token
    # TODO

    # Get the list of all channels the user is part of
    channels = get_user_channels_by_key("token", token)
    
    # return the list
    return { "channels": channels }