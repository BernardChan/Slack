# pylint: disable=W0105, W0622
import smtplib as smt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import database_files.database_retrieval as db
import helper_functions.interface_function_helpers as help
import helper_functions.auth_helper as auth
from error import InputError


"""
File for password resetting
"""


def send_email(message, email):
    """
    Sends an email with the specified message to the given email
    :param message: string for a piece of text to be sent via email
    :param email: string for an email to be sent a message to
    :return: returns nothing
    """
    # set up the SMTP server
    s = smt.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login("import.slack.h11a@gmail.com", "ImportSlack11")  # TODO: move this to another file

    msg = MIMEMultipart()
    msg["From"] = "import.slack.h11a@gmail.com"
    msg["To"] = email
    msg["Subject"] = "Password Reset from Slackr"
    msg.attach(MIMEText(message, "plain"))
    s.send_message(msg)
    del msg


def send_reset_token(email, user):
    """
    Sends an email with the reset token for resetting the password for the user
    with the corresponding email and attaches the token to the user in the database
    :param email: string for email
    :param user: dictionary containing a user's detail
    :return: returns nothing
    """

    reset_token = help.get_unique_id()
    message = f"""
    Your reset token is:
        {reset_token}
    """
    user["reset_code"] = reset_token
    send_email(message, email)


def send_warning_email(email):
    """
    Sends an email detailing that someone tried to reset the password for a Slackr user
    using this email
    :param email: string for email
    :return: returns nothing
    """
    message = """
    Someone has attempted to reset the password of a Slackr account using this Email. If this was
    you, please provide the Email that you use to log in to reset your password.
    """
    send_email(message, email)


def password_request(email):
    """
    Sends a code to the given email to reset the user's password
    :param email: string containing a user email
    :return: returns empty dictionary
    """

    user = db.get_users_by_key("email", email)
    if len(user) == 0:
        send_warning_email(email)

    else:
        send_reset_token(email, user[0])

    return {}


def password_reset(reset_code, new_password):
    """
    Resets the password if the given reset_code was correct
    :param reset_code: integer for verifying a user's identity without using a password
    :param new_password: string for a new password to overwrite the previous one
    :return: returns empty dictionary
    """
    try:
        reset_code = int(reset_code)
    except ValueError:
        print("couldn't convert to int")
        raise InputError("Invalid reset code provided")


    user = db.get_users_by_key("reset_code", reset_code)

    # Reset code wasn't found in the database
    if len(user) == 0:
        print("couldn't find user")
        raise InputError("Invalid reset code provided")

    # Validate password given
    print(f"new password given was {new_password}")
    auth.validate_password(new_password)
    user[0]["password"] = auth.hash_data(new_password)
    print(f"new password was {user[0]['password']}")

    return {}
