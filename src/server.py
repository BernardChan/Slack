import sys
import os.path
import threading
from json import dumps
from flask import Flask, request, redirect, url_for, send_from_directory
from flask_cors import CORS
import database_files.database as db
import interface_functions.other as other
import interface_functions.standup as su
import interface_functions.message as msg
import interface_functions.channel as ch
import interface_functions.channels as chs
import interface_functions.user as user
import interface_functions.admin_userpermission_change as admin
import interface_functions.user_remove as rmv
import interface_functions.channels as channels
import interface_functions.auth as auth
import interface_functions.workspace_reset as wr
import interface_functions.hangman as hang

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['POST'])
def echo():
    return dumps(request.form)


# # Remove this. This is purely for debugging.
# # It catches all routes that aren't implemented and echos
# #   what was received instead of throwing a 404 error.
# @APP.route("/<path:dummy>", methods=["GET", "POST", "PUT", "DELETE"])
# def catch_all(dummy):
#     # Ternary is too long for this if else
#     if request.method in ["POST", "PUT", "DELETE"]:
#         return dumps({"foobar": "testing"})
#     else:
#         return dumps(request.args)


@APP.route("/get/database", methods=["GET"])
def get_database():
    return dumps(db.DATABASE)


# ----------------------------------------------------------------------------------
# AUTH Routes
# ----------------------------------------------------------------------------------

@APP.route("/auth/register", methods=['POST'])
def auth_register():
    resp = request.get_json()
    email = resp["email"]
    password = resp["password"]
    name_first = resp["name_first"]
    name_last = resp["name_last"]
    return dumps(auth.auth_register(email, password, name_first, name_last))


@APP.route("/auth/login", methods=['POST'])
def auth_login():
    resp = request.get_json()
    email = resp["email"]
    password = resp["password"]
    return dumps(auth.auth_login(email, password))


@APP.route("/auth/logout", methods=['POST'])
def auth_logout():
    resp = request.get_json()
    token = resp["token"]
    return dumps(auth.auth_logout(token))


# ----------------------------------------------------------------------------------
# CHANNEL Routes
# ----------------------------------------------------------------------------------

# @APP.route("/channel/invite", methods=['POST'])
# def channel_invite():
#     resp = request.get_json()
#     token = resp["token"]
#     channel_id = resp["channel_id"]
#     u_id = resp["u_id"]
#     return dumps(ch.channel_invite(token, channel_id, u_id))


@APP.route("/channel/details", methods=['GET'])
def channel_details():
    resp = request.args

    # Get the relevant data from the response
    token = resp["token"]
    channel_id = int(resp["channel_id"])

    return dumps(ch.channel_details(token, channel_id))


@APP.route("/channel/messages", methods=['GET'])
def channel_messages():
    resp = request.args

    # Get the relevant data from the response
    token = resp["token"]
    channel_id = int(resp["channel_id"])
    start = int(resp["start"])

    return dumps(ch.channel_messages(token, channel_id, start))

# """
# @APP.route("/channel/leave", methods=['POST'])
# def channel_leave():
#     resp = request.get_json()
#     token = resp["token"]
#     channel_id = resp["channel_id"]
#     return dumps(ch.channel_leave(token, channel_id))
# """

# """
# @APP.route("/channel/join", methods=['POST'])
# def channel_join():
#     resp = request.get_json()
#     token = resp["token"]
#     channel_id = resp["channel_id"]
#     return dumps(ch.channel_join(token, channel_id))
# """


@APP.route("/channel/addowner", methods=['POST'])
def channel_addowner():
    resp = request.get_json()
    token = resp["token"]
    channel_id = resp["channel_id"]
    u_id = resp["u_id"]
    return dumps(ch.channel_addowner(token, channel_id, u_id))


@APP.route("/channel/removeowner", methods=['POST'])
def channel_removeowner():
    resp = request.get_json()
    token = resp["token"]
    channel_id = resp["channel_id"]
    u_id = resp["u_id"]
    return dumps(ch.channel_removeowner(token, channel_id, u_id))

# '''
# ----------------------------------------------------------------------------------
# CHANNELS Routes
# ----------------------------------------------------------------------------------
# '''
@APP.route("/channels/list", methods=['GET'])
def channels_list():
    token = request.args.get("token")

    return dumps(channels.channels_list(token))


@APP.route("/channels/listall", methods=['GET'])
def channels_listall():
    token = request.args.get("token")
    
    return dumps(channels.channels_listall(token))


@APP.route("/channels/create", methods=['POST'])
def channels_create():
    resp = request.get_json()

    # Get the relevant data from the response
    token = resp["token"]
    name = resp["name"]
    is_public = resp["is_public"]

    data = chs.channels_create(token, name, is_public)
    return dumps(data)

# '''
# ----------------------------------------------------------------------------------
# MESSAGE Routes
# ----------------------------------------------------------------------------------
# '''
@APP.route("/message/send", methods=['POST'])
def message_send():
    resp = request.get_json()

    # Get the relevant data from the response
    token = resp["token"]
    channel_id = int(resp["channel_id"])
    message = resp["message"]

    return dumps(msg.message_send(token, channel_id, message))


@APP.route("/message/sendlater", methods=['POST'])
def message_sendlater():
    resp = request.get_json()

    # Get the relevant data from the response
    token = resp["token"]
    channel_id = int(resp["channel_id"])
    message = resp["message"]
    time_sent = int(resp["time_sent"])

    return dumps(msg.send_later(token, channel_id, message, time_sent))


@APP.route("/message/react", methods=['POST'])
def message_react():
    resp = request.get_json()
    token = resp["token"]
    message_id = resp["message_id"]
    react_id = resp["react_id"]
    return dumps(msg.message_react(token, message_id, react_id))


@APP.route("/message/unreact", methods=['POST'])
def message_unreact():
    resp = request.get_json()
    token = resp["token"]
    message_id = resp["message_id"]
    react_id = resp["react_id"]
    return dumps(msg.message_unreact(token, message_id, react_id))


@APP.route("/message/pin", methods=['POST'])
def message_pin():
    resp = request.get_json()
    token = resp["token"]
    message_id = resp["message_id"]
    return dumps(msg.message_pin(token, message_id))


@APP.route("/message/unpin", methods=['POST'])
def message_unpin():
    resp = request.get_json()
    token = resp["token"]
    message_id = resp["message_id"]
    return dumps(msg.message_unpin(token, message_id))


@APP.route("/message/remove", methods=['DELETE'])
def message_remove():
    resp = request.get_json()
    token = resp["token"]
    message_id = resp["message_id"]
    return dumps(msg.message_remove(token, message_id))


@APP.route("/message/edit", methods=['PUT'])
def message_edit():
    resp = request.get_json()
    token = resp["token"]
    message_id = resp["message_id"]
    message = resp["message"]
    return dumps(msg.message_edit(token, message_id, message))


# '''
# ----------------------------------------------------------------------------------
# USER / PROFILE Routes
# ----------------------------------------------------------------------------------
# '''
@APP.route("/user/profile", methods=['GET'])
def user_profile():
    token = request.args.get("token")
    u_id = int(request.args.get("u_id"))

    return dumps(user.user_profile(token, u_id))


@APP.route("/user/profile/setname", methods=['PUT'])
def user_profile_setname():
    data = request.get_json()
    token = data["token"]
    name_first = data["name_first"]
    name_last = data["name_last"]

    return dumps(user.user_profile_setname(token, name_first, name_last))


@APP.route("/user/profile/setemail", methods=['PUT'])
def user_profile_setemail():
    data = request.get_json()
    token = data["token"]
    email = data["email"]

    return dumps(user.user_profile_setemail(token, email))


@APP.route("/user/profile/sethandle", methods=['PUT'])
def user_profile_sethandle():
    data = request.get_json()
    token = data["token"]
    handle_str = data["handle_str"]

    return dumps(user.user_profile_sethandle(token, handle_str))

@APP.route("/user/profile/uploadphoto", methods=['POST'])
def user_profile_uploadphoto():
    data = request.get_json()
    token = data["token"]
    img_url = data["img_url"]
    x_start = int(data["x_start"])
    y_start = int(data["y_start"])
    x_end = int(data["x_end"])
    y_end = int(data["y_end"])

    # saves the cropped image in database_files/user_images/<u_id>.jpg
    return dumps(user.user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end))

@APP.route("/userimages/<img_name>")
def get_profile_image(img_name):
    dirname = os.path.realpath(os.getcwd())
    return send_from_directory(f"{dirname}/database_files/user_images/", img_name)

# '''
# ----------------------------------------------------------------------------------
# USERS Routes
# ----------------------------------------------------------------------------------
# '''
@APP.route("/users/all", methods=['GET'])
def users_all():
    token = request.args.get("token")
    return dumps(other.users_all(token))

# '''
# ----------------------------------------------------------------------------------
# STANDUP Routes
# ----------------------------------------------------------------------------------
# '''
@APP.route("/standup/start", methods=['POST'])
def standup_start():
    resp = request.get_json()
    token = resp["token"]
    channel_id = int(resp["channel_id"])
    length = int(resp["length"])

    return dumps(su.standup_start(token, int(channel_id), int(length)))


@APP.route("/standup/active", methods=['GET'])
def standup_active():
    token = request.args.get("token")
    channel_id = request.args.get("channel_id")

    return dumps(su.standup_active(token, int(channel_id)))


@APP.route("/standup/send", methods=['POST'])
def standup_send():
    resp = request.get_json()
    token = resp["token"]
    channel_id = int(resp["channel_id"])
    message = resp["message"]

    return dumps(su.standup_send(token, channel_id, message))


# '''
# ----------------------------------------------------------------------------------
# OTHER Routes
# ----------------------------------------------------------------------------------
# '''
@APP.route("/search", methods=['GET'])
def search():
    query = request.args.get("query_str")
    token = request.args.get("token")

    return dumps(other.search(token, query))


@APP.route("/admin/userpermission/change", methods=['POST'])
def admin_userpermission_change():
    data = request.get_json()
    token = data["token"]
    u_id = int(data["u_id"])
    permission_id = int(data["permission_id"])

    return dumps(admin.admin_userpermission_change(token, u_id, permission_id))


@APP.route("/admin/user/remove", methods=["DELETE"])
def admin_user_remove():
    """
    Sends the DELETE request to
    remove the user with the given u_id from the database

    :return: Returns a json object containing the dictionary from user remove
    """
    data = request.get_json()
    token = data["token"]
    u_id = int(data["u_id"])

    return dumps(rmv.admin_user_remove(token, u_id))


@APP.route("/hangman/start", methods=["GET"])
def hangman_start():
    # data = request.get_json()
    token = request.args.get("token")
    channel_id = int(request.args.get("channel_id"))

    return dumps(hang.hangman_start(token, channel_id))


@APP.route("/hangman/guess", methods=["GET"])
def hangman_guess():
    token = request.args.get("token")
    channel_id = int(request.args.get("channel_id"))
    guess_letter = request.args.get("guess_letter")

    return dumps(hang.hangman_guess(token, channel_id, guess_letter))


@APP.route("/hangman/details", methods=["GET"])
def hangman_details():
    token = request.args.get("token")
    channel_id = int(request.args.get("channel_id"))

    return dumps(hang.hangman_details(token, channel_id))


@APP.route("/workspace/reset", methods=['POST'])
def workspace_reset():
    return dumps(wr.workspace_reset())


# Creates a thread for setting a schedule
def start_thread_helper():
    """
    Creates a thread to constantly check if a message needs to be sent from the message queue
    :return: returns nothing
    """
    t = threading.Thread(target=msg.set_sched)
    t.start()


def start_pickling_thread(length):
    t = threading.Thread(target=db.pickle_database_routinely, args=[length])
    t.start()


if __name__ == "__main__":
    # Create a thread for message_send_later()
    start_thread_helper()

    # Start pickling the database routinely
    db.unpickle_database()
    start_pickling_thread(length=10)

    # Start the server
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 42069))




