import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import interface_functions.other as other
import interface_functions.standup as su
import interface_functions.message as msg
import interface_functions.channel as ch
import interface_functions.channels as chs


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


@APP.route("/message/sendlater", methods=['POST'])
def message_sendlater():
    resp = request.get_json()

    # Get the relevant data from the response
    token = resp["token"]
    channel_id = int(resp["channel_id"])
    message = resp["message"]
    time_sent = int(resp["time_sent"])

    return dumps(msg.send_later(token, channel_id, message, time_sent))


@APP.route("/channel/messages", methods=['GET'])
def channel_messages():
    resp = request.args

    # Get the relevant data from the response
    token = resp["token"]
    channel_id = int(resp["channel_id"])
    start = int(resp["start"])

    return dumps(ch.channel_messages(token, channel_id, start))


@APP.route("/channel/details", methods=['GET'])
def channel_details():
    resp = request.args

    # Get the relevant data from the response
    token = resp["token"]
    channel_id = int(resp["channel_id"])

    return dumps(ch.channel_details(token, channel_id))


@APP.route("/message/send", methods=['POST'])
def message_send():
    resp = request.get_json()

    # Get the relevant data from the response
    token = resp["token"]
    channel_id = int(resp["channel_id"])
    message = resp["message"]

    return dumps(msg.message_send(token, channel_id, message))


@APP.route("/channels/create", methods=['POST'])
def channels_create():
    resp = request.get_json()

    # Get the relevant data from the response
    token = resp["token"]
    name = resp["name"]
    is_public = resp["is_public"]

    return dumps(chs.channels_create(token, name, is_public))


if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 42069))
