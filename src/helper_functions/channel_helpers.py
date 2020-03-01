# Functions and variables that are used as input for testing slakr functions
# Contains variables for:
#   2 users, one of which is part of a channel
#   a channel with 1 member in it
#   function that returns a boolean on whether a user is part of the above channel

import channels as chs
import channel as ch
import auth

# Create the slackr owner that is not part of the channel
slackr_owner = auth.auth_register("ownertest@test.tst", "password", "owner", "lastname")
slackr_owner_id = slackr_owner["u_id"]
slackr_owner_token = slackr_owner["token"]

# Create a channel owner
chan_owner = auth.auth_register("membertest2@test.tst", "password2", "name2", "lastname2")
chan_owner_id = chan_owner["u_id"]
chan_owner_token = chan_owner["token"]

# Create a normal user that is not part of the channel
member = auth.auth_register("membertest2@test.tst", "password2", "name2", "lastname2")
member_id = chan_owner["u_id"]
member_token = chan_owner["token"]

# Create public channel with the channel owner as the sole person in it
channel_id = chs.channels_create(chan_owner_token, "channel1", True)

# Get details of the channel
channel = ch.channel_details(chan_owner, channel_id)
channel_name = channel["name"]
channel_owner = channel["owner_members"]
channel_members = channel["all_members"]  # array of {u_id, name_first, name_last}


# Returns true if given user ID is part of the channel, else false
def is_member(user_id):
    return any([user_id == person["u_id"] for person in channel_members])
