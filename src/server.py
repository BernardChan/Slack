import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import interface_functions.other as other
import interface_functions.standup as su

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


# TODO: Remove this. This is purely for debugging. It catches all routes that aren't implemented and echos
#   what was received instead of throwing a 404 error.
@APP.route("/<path:dummy>", methods=["GET", "POST", "PUT", "DELETE"])
def catch_all(dummy):
    # Ternary is too long for this if else
    if request.method in ["POST", "PUT", "DELETE"]:
        return dumps(request.form)
    else:
        return dumps(request.args)



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



if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 42069))
