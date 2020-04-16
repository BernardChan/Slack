# Functions and variables that are used as input for testing slackr functions

# Usage:
#   There are 3 users: "slackr_owner", "chan_owner", "member" (slackr owner, channel owner, default member)
#       they all have their own "_token" and "_id"
#       e.g. "slackr_owner_token" and "member_id" can both be used by importing this file
#       only chan_owner is part of a channel, you'll have to channel_invite() slackr_owner and member

#   There are 2 channels: "channel_id" and "private_channel_id"
#       - They are a public channel and private channel respectively
#       - You can use them anywhere a channel_id is required
#       They have a "_name", "_owner", "_members" variable attached
#       e.g. "private_channel_name" or "channel_members". These are from the dictionary returned from channel_details()

#   There are 2 functions: "is_member" and "is_owner"
#       They check if a given user_id is a member or an owner of a channel respectively
#       they both except a "user_id" and "is_public"
#           "is_public" is a boolean: "True" or "False"
#               - gives which channel to check (public or private channels respectively)
#           user_id is the id of the user (e.g. "member_id")
#   e.g. is_member(chan_owner_id, True) # returns "True", since chan_owner is a member of the public channel
#   e.g. is_member(slackr_owner_id, False) # returns "False", since slackr_owner is not member of the private channel

from interface_functions import auth, channel as ch, channels as chs
from interface_functions.workspace_reset import workspace_reset

invalid_channel_id, invalid_user_id, slackr_owner, slackr_owner_id, slackr_owner_token, chan_owner, \
        chan_owner_id, chan_owner_token, member, member_id, member_token, channel_id, private_channel_id, channel, \
        channel_name, channel_owner, channel_members, private_channel, private_channel_name, private_channel_owner, \
        private_channel_members = (None, )*21


def init_helper():
    # workspace_reset()

    global invalid_channel_id, invalid_user_id, slackr_owner, slackr_owner_id, slackr_owner_token, chan_owner, \
        chan_owner_id, chan_owner_token, member, member_id, member_token, channel_id, private_channel_id, channel, \
        channel_name, channel_owner, channel_members, private_channel, private_channel_name, private_channel_owner, \
        private_channel_members

    # Invalid channel ID
    invalid_channel_id = -100000

    # invalid user_id
    invalid_user_id = -100000

    # Create the slackr owner that is not part of the channel
    slackr_owner = auth.auth_register("ownertest@test.tst", "password", "owner", "lastname")
    slackr_owner_id = slackr_owner["u_id"]
    slackr_owner_token = slackr_owner["token"]

    # Create a channel owner
    chan_owner = auth.auth_register("membertest2@test.tst", "password2", "name2", "lastname2")
    chan_owner_id = chan_owner["u_id"]
    chan_owner_token = chan_owner["token"]

    # Create a normal user that is not part of the channel
    member = auth.auth_register("member@test.tst", "password2", "name2", "lastname2")
    member_id = member["u_id"]
    member_token = member["token"]

    # Create public channel with the channel owner as the sole person in it
    channel_id = chs.channels_create(chan_owner_token, "channel1", True)["channel_id"]
    private_channel_id = chs.channels_create(chan_owner_token, "channel1", False)["channel_id"]

    # Get details of the public channel
    channel = ch.channel_details(chan_owner_token, channel_id)
    channel_name = channel["name"]
    channel_owner = channel["owner_members"]
    channel_members = channel["all_members"]  # array of {u_id, name_first, name_last}

    # Get details of the private channel
    private_channel = ch.channel_details(chan_owner_token, channel_id)
    private_channel_name = channel["name"]
    private_channel_owner = channel["owner_members"]
    private_channel_members = channel["all_members"]  # array of {u_id, name_first, name_last}

# TODO: remove this
import database_files.database_retrieval as db

# Returns true if given user ID is part of the channel, else false
def is_member(user_id, is_public):
    global channel_id, private_channel_id

   
    if is_public:
        channel_members = db.get_channels_by_key('channel_id', channel_id)[0]["members"]

        return any([user_id == person["u_id"] for person in channel_members])
    else:
        private_channel_members = db.get_channels_by_key('channel_id', private_channel_id)[0]["members"]
        return any([user_id == person["u_id"] for person in private_channel_members])


def is_owner(user_id, is_public):
    global channel_owner, private_channel_owner
    if is_public:
        channel_members = db.get_channels_by_key('channel_id', channel_id)[0]["owner_members"]

        return any([user_id == person["u_id"] for person in channel_members])
    else:
        private_channel_members = db.get_channels_by_key('channel_id', private_channel_id)[0]["owner_members"]
        return any([user_id == person["u_id"] for person in private_channel_members])


# Checks if a function is implemented or not
# Accepts (functionName, arg1, arg2, ...)
# Make sure the args are INCORRECT - e.g. if a function expects a string, give
# an integer so it doesn't excecute the function and start adding data to database
# Super crude way of doing this but it's necessary due to how our project is marked.
def isFunctionImplemented(*args):

    # Exception shouldn't be thrown by the function if it isn't implemented
    try:
        functionName, *functionArgs = args
        if functionName(*functionArgs) == "Not Implemented":
            return False
    except:
        # Exception was thrown due to incorrect input (as desired) meaning the
        # function is implemented
        return True
