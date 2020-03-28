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
member_id = chan_owner["u_id"]
member_token = chan_owner["token"]

# Create public channel with the channel owner as the sole person in it
channel_id = chs.channels_create(chan_owner_token, "channel1", True)
private_channel_id = chs.channels_create(chan_owner_token, "channel1", False)

# Get details of the public channel
channel = ch.channel_details(chan_owner, channel_id)
channel_name = channel["name"]
channel_owner = channel["owner_members"]
channel_members = channel["all_members"]  # array of {u_id, name_first, name_last}

# Get details of the private channel
private_channel = ch.channel_details(chan_owner, channel_id)
private_channel_name = channel["name"]
private_channel_owner = channel["owner_members"]
private_channel_members = channel["all_members"]  # array of {u_id, name_first, name_last}


# Returns true if given user ID is part of the channel, else false
def is_member(user_id, is_public):
    if is_public:
        return any([user_id == person["u_id"] for person in channel_members])
    else:
        return any([user_id == person["u_id"] for person in private_channel_members])


def is_owner(user_id, is_public):
    if is_public:
        return any([user_id == owner["u_id"] for owner in channel_owner])
    else:
        return any([user_id == owner["u_id"] for owner in private_channel_owner])

