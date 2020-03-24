import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import interface_functions.user as user
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

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
