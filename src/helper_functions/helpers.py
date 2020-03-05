import pytest
import auth
import channels as chs
import channel as ch

# TODO: address the warning since I'm using a pytest.fixture as a function in this file. It works fine,
#  but need to see what tutor says.


# Get Invalid IDs
@pytest.fixture
def invalid_channel_id():
    return -100000


@pytest.fixture
def invalid_user_id():
    return -100000


############################
# Functions for token/u_id #
############################

@pytest.fixture
# Create a default member that doesn't have special permissions
def get_member():
    data = auth.auth_register("defaultmember@test.com", "password1", "default", "member")
    return data["u_id"], data["token"]

# Create the slackr owner but isn't part of any channels
@pytest.fixture
def get_slackr_owner():
    slackr_owner = auth.auth_register("slackrownertest@test.tst", "password", "slackr", "owner")
    return slackr_owner["u_id"], slackr_owner["token"]


# Create a channel owner
@pytest.fixture
def get_channel_owner():
    chan_owner = auth.auth_register("ownertest2@test.tst", "password2", "channel", "owner")
    return chan_owner["u_id"], chan_owner["token"]

##########################
# Functions for channels #
##########################

# Create public channel with the channel owner as the sole person in it
@pytest.fixture
def get_public_channel():
    # TODO: verify that this function can call the other functions in this file
    chan_owner_id, chan_owner_token = get_channel_owner()
    channel_name = "publicChannel"
    channel_id = chs.channels_create(chan_owner_token, channel_name, True)

    return channel_name, channel_id


@pytest.fixture
def get_private_channel():
    chan_owner_id, chan_owner_token = get_channel_owner()
    private_channel_name = "privateChannel"
    private_channel_id = chs.channels_create(chan_owner_token, private_channel_name, False)

    return private_channel_name, private_channel_id


# Get details of the public channel - returns "name", "owner_members", "all_members"
# look up specification for usage and return types
@pytest.fixture
def get_channel_details():
    chan_owner_id, chan_owner_token = get_channel_owner()
    channel_name, channel_id = get_public_channel()
    channel = ch.channel_details(chan_owner_token, channel_id)

    return channel["name"], channel["owner_members"], channel["all_members"]


# Get details of the private channel - returns "name", "owner_members", "all_members"
# look up specification for usage and return types
@pytest.fixture
def get_private_channel_details():
    chan_owner_id, chan_owner_token = get_channel_owner()
    channel_name, channel_id = get_private_channel()
    channel = ch.channel_details(chan_owner_token, channel_id)

    return channel["name"], channel["owner_members"], channel["all_members"]

######################################################################
# Functions to check if a user is part of the private/public channel #
######################################################################


# Returns true if given user ID is part of the channel, else false
@pytest.fixture
def is_member(user_id, is_public):
    all_members = get_channel_details()[2]
    p_all_members = get_private_channel_details()[2]

    if is_public:
        return any([user_id == person["u_id"] for person in all_members])
    else:
        return any([user_id == person["u_id"] for person in p_all_members])


@pytest.fixture
def is_owner(user_id, is_public):
    all_members = get_channel_details()[2]
    p_all_members = get_private_channel_details()[2]

    if is_public:
        return any([user_id == owner["u_id"] for owner in all_members])
    else:
        return any([user_id == owner["u_id"] for owner in p_all_members])

