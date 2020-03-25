import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import interface_functions.other as other
import interface_functions.standup as su
import interface_functions.user as user
import interface_functions.admin_userpermission_change as admin
import interface_functions.channels as channels

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
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })


@APP.route("/search", methods=['GET'])
def search():
    query = request.args.get("query_str")
    token = request.args.get("token")

    return dumps(other.search(token, query))


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


@APP.route("/user/profile", methods=['GET'])
def user_profile():
    token = request.args.get("token")
    u_id = request.args.get("u_id")

    return dumps(user.user_profile(token, u_id))

@APP.route("user/profile/setname", methods=['PUT'])
def user_profile_setname():
    data = request.get_json()
    token = data["token"]
    name_first = data["name_first"]
    name_last = data["name_last"]

    return dumps(user.user_profile_setname(token, name_first, name_last))

@APP.route("user/profile/setemail", methods=['PUT'])
def user_profile_setemail():
    data = request.get_json()
    token = data["token"]
    email = data["email"]

    return dumps(user.user_profile_setemail(token, email))

@APP.route("user/profile/sethandle", methods=['PUT'])
def user_profile_sethandle():
    data = request.get_json()
    token = data["token"]
    handle_str = data["handle_str"]

    return dumps(user.user_profile_sethandle(token, handle_str))

@APP.route("admin/userpermission/change", methods=['POST'])
def admin_userpermission_change():
    data = request.get_json()
    token = data["token"]
    u_id = data["u_id"]
    permission_id = data["permission_id"]

    return dumps(admin.admin_userpermission_change(token, u_id, permission_id))

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 42069))
