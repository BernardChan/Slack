import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import interface_functions.other as other
import interface_functions.standup as su
import interface_functions.channel as chan

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

# channel functions
@APP.route("/channel/invite", methods=['POST'])
def channel_invite():
    resp = request.get_json()
    token = resp["token"]
    channel_id = int(resp["channel_id"])
    u_id = int(resp["u_id"])
    
    return dumps(chan.channel_invite(token, channel_id, u_id))

@APP.route("/channel/leave", methods=['POST'])
def channel_leave():
    resp = request.get_json()
    token = resp["token"]
    channel_id = int(resp["channel_id"])

    return dumps(chan.channel_leave(token, channel_id)

@APP.route("/channel/join", methods=['POST'])
def channel_join():
    resp = request.get_json()
    token = resp["token"]
    channel_id = int(resp["channel_id"])

    return dumps(chan.channel_join(token, channel_id)

@APP.route("/channel/addowner", methods=['POST'])
def channel_addowner():
    resp = request.get_json()
    token = resp["token"]
    channel_id = int(resp["channel_id"])
    u_id = int(resp["u_id"])
    
    return dumps(chan.channel_addowner(token, channel_id, u_id))


@APP.route("/channel/removeowner", methods=['POST'])
def channel_removeowner():
    resp = request.get_json()
    token = resp["token"]
    channel_id = int(resp["channel_id"])
    u_id = int(resp["u_id"])
    
    return dumps(chan.channel_removeowner(token, channel_id, u_id))

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 42069))
