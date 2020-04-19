"""
File for functions relating to user profiles in the slackr app
"""

import re
import urllib.request
import os.path
from PIL import Image, UnidentifiedImageError
from error import InputError
from database_files.database_retrieval import get_users_by_key
import database_files.database as db
from helper_functions.interface_function_helpers import is_valid_token, get_unique_id

def user_profile(token, u_id):
    """
    For a valid user returns information about them
    :param token: authorised user's identifier
    :param u_id: user id for which info is returned
    :return: returns dictionary containing u_id, email, name_first, name_last, handle_str
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

    return {"user": user}


def user_profile_setname(token, name_first, name_last):
    """
    Update a user's first and last name
    :param token: authorised user's identifier
    :param name_first: new first name to update with
    :param name_last: new last name to update with
    :return: returns nothing
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
    Updates the a user's email address
    :param token: authorised user's identifier
    :param email: new email to update with
    :return: returns nothing
    """
    # Raise an AccessError if not a valid token
    is_valid_token(token)

    def valid_email(string):
        """
        Helper function to determine if an email is valid
        """
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
    Update a user's handle (display name)
    :param token: authorised user's identifier
    :param handle_str: new handle string
    :return: returns nothing
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
    Helper function checking if crop values are within image dimensions
    """
    if x_start < 0 or x_start > width:
        raise InputError(description="x_start is not within dimensions of the image!")
    elif x_end < 0 or x_end > width:
        raise InputError(description="x_end is not within dimensions of the image!")
    elif y_start < 0 or y_start > height:
        raise InputError(description="y_start is not within dimensions of the image!")
    elif y_end < 0 or y_end > height:
        raise InputError(description="y_end is not within dimensions of the image!")
    elif x_start >= x_end:
        raise InputError(description="x_start cannot be greater than or equal to x_end!")
    elif y_start >= y_end:
        raise InputError(description="y_start cannot be greater than or equal to y_end!")

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end): # pylint: disable=too-many-arguments
    """
    Given a jpeg image URL, crop the image and store it locally.
    :param token: authorised user's identifier
    :param img_url: URL for a jpeg image
    :param x_start: x coordinate start of crop
    :param y_start: y coordinate start of crop
    :param x_end: x coordinate end of crop
    :param y_end: y coordinate end of crop
    :return: returns nothing
    """
    # Raise AccessError for invalid token
    is_valid_token(token)

    # Raise InputError for img_url returning a HTTP status other than 200
    if urllib.request.urlopen(img_url).getcode() != 200:
        raise InputError(description="Image URL returns a HTTP status other than 200!")

    # Open the image in RGB mode
    try:
        img = Image.open(urllib.request.urlopen(img_url))
    except UnidentifiedImageError:
        raise InputError(description="Url given is not a JPG image!")

    # Raise InputError if the image isn't a jpg
    if not img.format == "JPEG":
        raise InputError(description="Image uploaded is not a JPG!")

    width, height = img.size
    is_crop_within_boundaries(x_start, y_start, x_end, y_end, width, height)

    # Crop the image
    img = img.crop((x_start, y_start, x_end, y_end))

    # get the u_id of the user by token
    u_id = get_users_by_key("token", token)[0]["u_id"]
    # generate unique id for image
    img_id = get_unique_id()
    # save the image to database_files/user_images/{img_id}.jpg
    dirname = os.path.dirname(__file__)
    # make the user_images directory if it doesn't exist yet
    if not os.path.exists(f"{dirname}/../database_files/user_images"):
        os.makedirs(f"{dirname}/../database_files/user_images")
    # save the image
    img.save(os.path.join(dirname, "../database_files/user_images/", f"{img_id}.jpg"), "JPEG")

    # update the profile_img_url key in user dict
    for profile in db.DATABASE["users"]:
        if profile["u_id"] == u_id:
            # assumes that the port is 42069
            profile["profile_img_url"] = f"http://localhost:42069/userimages/{img_id}.jpg"
            break

    return {}
