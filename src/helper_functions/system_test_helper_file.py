# Functions and variables that are used as input for testing slackr functions

# Usage: Refer to test_helper_file. I am reimplementing them with HTTP requests as per Rob's instruction

import requests

# Invalid channel ID
invalid_channel_id = -100000

# invalid user_id
invalid_user_id = -100000

# Global constant for the URL to prevent having to retype it every time
BASE_URL = "http://127.0.0.1:42069"


# Usage:
# make_    _request(route, dict)
#    Accepts `route` as a string (HTTP route e.g. channel/leave, message/send etc.)
#    Accepts a `dict` dictionary, containing the required inputs for the function
#       e.g. {"token": token, "u_id": id}

# ============================== IMPORTANT ==============================
# For POST/PUT/DELETE requests, use request.form NOT request.args in
# the server to get data. For GET requests, use request.args like normal.
# =======================================================================


# Make GET request
def make_get_request(route, dict):
    req = requests.get(f"{BASE_URL}/{route}", params=dict)
    return req.json()


# Make a POST request
def make_post_request(route, dict):
    req = requests.post(f"{BASE_URL}/{route}", data=dict)
    return req.json()


# Make DELETE request
def make_delete_request(route, dict):
    req = requests.delete(f"{BASE_URL}/{route}", data=dict)
    return req.json()


# Make PUT request
def make_put_request(route, dict):
    req = requests.put(f"{BASE_URL}/{route}", data=dict)
    return req.json()


# Reset the database
def reset():
    requests.get(f"{BASE_URL}/workspace/reset")


# TODO: move all of these into functions so as not to call all functions whenever this file is called
# Create the slackr owner that is not part of a channel
# Returns tuple with (u_id, token)
def get_slackr_owner():
    user = make_post_request("auth/register", {
        "email": "ownertest@test.tst",
        "password": "password",
        "name_first": "slackr",
        "name_last": "owner"
    })
    return user["u_id"], user["token"]


# Create a channel owner
def get_channel_owner():
    user = make_post_request("auth/register", {
        "email": "chanowner@test.tst",
        "password": "password",
        "name_first": "channel",
        "name_last": "owner"
    })
    return user["u_id"], user["token"]


# Create a normal user that is not part of the channel
def get_member():
    user = make_post_request("auth/register", {
        "email": "user@test.tst",
        "password": "password",
        "name_first": "user",
        "name_last": "member"
    })
    return user["u_id"], user["token"]


# Create public channel with the channel owner as the sole person in it
# Note: You need to pass in channel owner's token here
# TODO: figure out a better alternative to forcing us to pass in
#   channel owner's token every time. Maybe get it directly from database?
def create_public_channel(token):
    channel = make_post_request("channels/create", {
        "token": token,
        "name": "public_channel",
        "is_public": True
    })
    return channel["channel_id"]


# Note: You need to pass in channel owner's token here
# TODO: figure out a better alternative to forcing us to pass in
#   channel owner's token every time. Maybe get it directly from database?
def create_private_channel(token):
    channel = make_post_request("channels/create", {
        "token": token,
        "name": "private_channel",
        "is_public": False
    })
    return channel["channel_id"]


# Get details of the public channel
def get_public_channel_details(token, channel_id):
    channel = make_get_request("channel/details", {"token": token, "channel_id": channel_id})
    return channel["name"], channel["owner"], channel["members"]


# Get details of the private channel
def get_private_channel_details(token, channel_id):
    channel = make_get_request("channel/details", {"token": token, "channel_id": channel_id})
    return channel["name"], channel["owner"], channel["members"]


# TODO: update these functions based on whether we can access the database directly or not
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


if __name__ == "__main__":
    foo = make_get_request("easdcho", {"token": "asd", "ch_id": 1})
    print(foo)

    # print(foo["token"])
