# Functions and variables that are used as input for testing slakr functions
# Contains variables for:
#   2 users, one of which is part of a channel
#   a channel with 1 member in it
#   function that returns a boolean on whether a user is part of the above channel

import channels as chs
import channel as ch
import auth

# Create a user that is part of a channel
login = auth.auth_register("test@test.tst", "password", "name", "lastname")
u_id = login["u_id"]
token = login["token"]

# Create a second user that is not part of the channel
login2 = auth.auth_register("test2@test.tst", "password2", "name2", "lastname2")
u_id2 = login2["u_id"]
token2 = login2["token"]

# Create public channel with user (token) in it
channel_id = chs.channels_create(token, "channel1", True)

# Get details of the channel
channel = ch.channel_details(token, channel_id)
channel_name = channel["name"]
channel_owner = channel["owner_members"]
channel_members = channel["all_members"]  # array of {u_id, name_first, name_last}


# Returns true if given user ID is part of the channel, else false
def is_member(user_id):
    return any([user_id == member["u_id"] for member in channel_members])
