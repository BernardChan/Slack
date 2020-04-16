"""
user/profile/... functions for slackr app
"""

import re
import urllib.request
import os.path
from PIL import Image
from error import InputError
#from database_files.database_retrieval import get_users
from database_files.database_retrieval import get_users_by_key
from helper_functions.interface_function_helpers import is_valid_token
import database_files.database as db

def user_profile(token, u_id):
    """
    For a valid user, returns information about their user id, email, first name,
        last name, and handle
    Input: token, u_id
    Output: {u_id, email, name_first, name_last, handle_str}
    """

    # Raise an AccessError if not a valid token
    is_valid_token(token)

    # Go through all users and collect the correct user dictionary
    # If no users found with u_id, invalid u_id because user does not exist
    if get_users_by_key("u_id", u_id) == []:
        raise InputError(description="Invalid user id!")
    # full user also contains permission_id, password, token, etc.
    full_user = get_users_by_key("u_id", u_id)[0]

    user = {
        "u_id": full_user["u_id"],
        "email": full_user["email"],
        "name_first": full_user["name_first"],
        "name_last": full_user["name_last"],
        "handle_str": full_user["handle_str"],
        "profile_img_url": full_user["profile_img_url"]
    }

    return {user}


def user_profile_setname(token, name_first, name_last):
    """
    Update the authorised user's first and last name
    Input: token, name_first, name_last
    Output: {}
    """

    # Raise an AccessError if not a valid token
    is_valid_token(token)

    # Raise an InputError if either name is out of bounds
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(description="First name is not between 1 and 50 characters!")
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(description="Last name is not between 1 and 50 characters!")

    # Get the user with the matching u_id by token
    match = get_users_by_key("token", token)
    u_id = match[0]["u_id"]
    # Update first and last name for the correct user
    for profile in db.DATABASE["users"]:
        if profile["u_id"] == u_id:
            profile["name_first"] = name_first
            profile["name_last"] = name_last
            break

    return {}


def user_profile_setemail(token, email):
    """
    Updates the authorised user's email address
    Input: token, email
    Output: {}
    """

    # Raise an AccessError if not a valid token
    is_valid_token(token)

    # Inner helper function for determining a valid email
    def valid_email(string):
        # Make a regular expression for validating email
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$' # pylint: disable=anomalous-backslash-in-string
        # Pass the regular expression and the string using search() to check if valid
        return re.search(regex, string)
    # Raise an InputError if not a valid email
    if not valid_email(email):
        raise InputError(description="Invalid email!")

    # Raise an InputError if email is being used by another user
    # if get_users_by_key doesn't return an empty list
    if get_users_by_key("email", email) != []:
        raise InputError(description="Email address in use by another user!")

    # Get the user with the matching u_id by token
    match = get_users_by_key("token", token)
    u_id = match[0]["u_id"]
    # Update email for the correct user
    for profile in db.DATABASE["users"]:
        if profile["u_id"] == u_id:
            profile["email"] = email
            break

    return {}


def user_profile_sethandle(token, handle_str):
    """
    Update the authorised user's handle (display name)
    Input: token, handle_str
    Output: {}
    """

    # Raise an AccessError if not a valid token
    is_valid_token(token)

    # Raise an InputError if either name is out of bounds
    if len(handle_str) < 2 or len(handle_str) > 20:
        raise InputError(description="Handle (display name) is not between 2 and 20 characters!")

    # Raise an input error if handle is being used by another user
    # if get_users_by_key doesn't return an empty list
    if get_users_by_key("handle_str", handle_str) != []:
        raise InputError(description="Handle (display name) in use by another user!")

    # Get the user with the matching u_id by token
    match = get_users_by_key("token", token)
    u_id = match[0]["u_id"]
    # Update handle for the correct user
    for profile in db.DATABASE["users"]:
        if profile["u_id"] == u_id:
            profile["handle_str"] = handle_str
            break

    return {}

def is_crop_within_boundaries(x_start, y_start, x_end, y_end, width, height): # pylint: disable=too-many-arguments
    """
    Helper function to raise InputError if x_start, y_start, x_end, or y_end
    aren't in the dimensions of the image in the url. Also if x_start or y_start
    are > then x_end or y_end respectively.
    """
    if x_start < 0 or x_start > width:
        raise InputError(description="x_start is not within dimensions of the image!")
    elif x_end < 0 or x_end > width:
        raise InputError(description="x_end is not within dimensions of the image!")
    elif y_start < 0 or y_start > height:
        raise InputError(description="y_start is not within dimensions of the image!")
    elif y_end < 0 or y_end > height:
        raise InputError(description="y_end is not within dimensions of the image!")
    elif x_start > x_end:
        raise InputError(description="x_start cannot be greater than x_end!")
    elif y_start > y_end:
        raise InputError(description="y_start cannot be greater than y_end!")

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end): # pylint: disable=too-many-arguments
    """
    Given a URL of an image on the internet, crops the image within bounds
        (x_start, y_start) and (x_end, y_end). Then stores the image in
        database_files/user_images/<u_id>.jpg
    Input: token, img_url, x_start, y_start, x_end, y_end
    Output: {}
    """
    # Raise AccessError for invalid token
    is_valid_token(token)

    # Raise InputError for img_url returning a HTTP status other than 200
    if urllib.request.urlopen(img_url).getcode() != 200:
        raise InputError(description="Image URL returns a HTTP status other than 200!")

    # Raise InputError if image isn't a jpg
    if not img_url.endswith(".jpg"):
        raise InputError(description="Image uploaded is not a JPG!")

    # Open the image in RGB mode
    img = Image.open(urllib.request.urlopen(img_url))
    width, height = img.size
    is_crop_within_boundaries(x_start, y_start, x_end, y_end, width, height)

    # Crop the image
    img = img.crop((x_start, y_start, x_end, y_end))

    # get the u_id of the user by token
    u_id = get_users_by_key("token", token)[0]["u_id"]
    # save the image to database_files/user_images/{u_id}.jpg
    dirname = os.path.dirname(__file__)
    img.save(os.path.join(dirname, "../database_files/user_images/", f"{u_id}.jpg"), "JPEG")

    # update the profile_img_url key in user dict
    for profile in db.DATABASE["users"]:
        if profile["u_id"] == u_id:
            # assumes that the port is 42069
            profile["profile_img_url"] = f"http://localhost:42069/userimages/{u_id}.jpg"
            break

    return {}
