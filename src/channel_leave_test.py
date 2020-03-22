import json
import requests
import urllib
import urllib.parse
import helper_functions.test_helper_file as ch

# TODO: move BASE_URL to the helper file
BASE_URL = 'http://127.0.0.1:8080'
HTTP_ROUTE = "channel/leave"

# Reset the database
def reset():
    requests.get(f"{BASE_URL}/workspace/reset")


# Make a post request
# Accepts route (HTTP route e.g. channel/leave, message/send etc.)
# Accepts a dict, containing the required inputs for the function
def make_post_request(route, dict):

    # Make the http POST request and return a dictionary with the response
    req = requests.post(f"{BASE_URL}/{route}", json=dict)
    return req.json()


# Helper function that asserts that a member left a channel
def assert_user_leave(data, user_token, user_id, is_public):
    # Check that user is actually part of the channel - if this fails, problem with dependencies
    assert(ch.is_member(user_id, is_public))

    make_post_request("channel/leave", data) if is_public else make_post_request("channel/leave", data)

    # Assert that user is no longer a member
    assert(not ch.is_member(user_id, is_public))


def test_leave_slackr_owner():
    reset()

    # TODO: use helper file in helper_functions to get the token and channel_id
    data = {
        "token": token,
        "channel_id": channel_id
    }

    # TODO: import the relevant token/u_id and make sure they're from the public and private channels
    assert_user_leave(data, token, u_id, True)
    assert_user_leave(data, token, u_id, False)
    # TODO: check the database to see if the user has been removed





    queryString = urllib.parse.urlencode({
        'uc' : False,
    })
    r = requests.get(f"{BASE_URL}/info?{queryString}")
    payload = r.json()
    assert payload['firstName'] == ''
    assert payload['lastName'] == ''







    queryString = urllib.parse.urlencode({
        'uc' : False,
    })
    r = requests.get(f"{BASE_URL}/info?{queryString}")
    payload = r.json()
    assert payload['firstName'] == 'HAYDEN'
    assert payload['lastName'] == 'SMITH'
