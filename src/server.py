import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError

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


if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 42069))
