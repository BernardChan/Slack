# Functions for standup_active
import database_files.database_retrieval as db
import helper_functions.interface_function_helpers as help


# Returns info about a standup in the given channel
# TODO: Not sure what the token is for
#   Probably should throw an error if authorised user is not part of the channel_id
def standup_active(token, channel_id):

    # Check for errors
    help.check_channel_validity(channel_id)

    # Retrieve and return the relevant information from the database
    standup = db.get_channel_standup(channel_id)
    is_active = standup["active"]
    time_finish = standup["time_finish"]

    return {"is_active": is_active, "time_finish": time_finish}