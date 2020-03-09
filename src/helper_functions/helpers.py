import pytest
import auth
import channels as chs
import channel as ch

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
def member():
    data = auth.auth_register("defaultmember@test.com", "password1", "default", "member")
    return data["u_id"], data["token"]

# Create the slackr owner but isn't part of any channels
@pytest.fixture
def slackr_owner():
    slackr_owner = auth.auth_register("slackrownertest@test.tst", "password", "slackr", "owner")
    return slackr_owner["u_id"], slackr_owner["token"]


# Create a channel owner
@pytest.fixture
def channel_owner():
    chan_owner = auth.auth_register("ownertest2@test.tst", "password2", "channel", "owner")
    return chan_owner["u_id"], chan_owner["token"]

##########################
# Functions for channels #
##########################

# Create public channel with the channel owner as the sole person in it
@pytest.fixture
def public_channel():
    # TODO: verify that this function can call the other functions in this file
    chan_owner_id, chan_owner_token = channel_owner()
    channel_name = "publicChannel"
    channel_id = chs.channels_create(chan_owner_token, channel_name, True)

    return channel_name, channel_id


@pytest.fixture
def private_channel():
    chan_owner_id, chan_owner_token = channel_owner()
    private_channel_name = "privateChannel"
    private_channel_id = chs.channels_create(chan_owner_token, private_channel_name, False)

    return private_channel_name, private_channel_id


# Get details of the public channel - returns "name", "owner_members", "all_members"
# look up specification for usage and return types
@pytest.fixture
def channel_details():
    chan_owner_id, chan_owner_token = channel_owner()
    channel_name, channel_id = public_channel()
    channel = ch.channel_details(chan_owner_token, channel_id)

    return channel["name"], channel["owner_members"], channel["all_members"]


# Get details of the private channel - returns "name", "owner_members", "all_members"
# look up specification for usage and return types
@pytest.fixture
def private_channel_details():
    chan_owner_id, chan_owner_token = channel_owner()
    channel_name, channel_id = private_channel()
    channel = ch.channel_details(chan_owner_token, channel_id)

    return channel["name"], channel["owner_members"], channel["all_members"]


######################################################################
# Functions to check if a user is part of the private/public channel #
######################################################################

# Returns true if given user ID is part of the channel, else false
# Note: Closure (nested function) is used so that we can pass in args
#   into is_member()/is_owner() when it's used as a fixture
@pytest.fixture
def is_member():
    def _params(user_id, is_public):
        all_members = channel_details()[2]
        p_all_members = private_channel_details()[2]

        if is_public:
            return any([user_id == person["u_id"] for person in all_members])
        else:
            return any([user_id == person["u_id"] for person in p_all_members])
    return _params


@pytest.fixture
def is_owner():
    def _params(user_id, is_public):
        all_members = channel_details()[2]
        p_all_members = private_channel_details()[2]

        if is_public:
            return any([user_id == owner["u_id"] for owner in all_members])
        else:
            return any([user_id == owner["u_id"] for owner in p_all_members])
    return _params
