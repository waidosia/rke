import random
import time
import flask
from flask import request

server = flask.Flask(__name__)
date = int(time.time())
num = random.randint(99999, 999999)


@server.route("/api", methods=["POST"])
def api():
    global date
    global num
    passwd = request.values.get("passwd")
    if int(time.time()) - date >= 60:
        date = int(time.time())
        num = random.randint(99999, 999999)
    if passwd == "password":
        print(num)
        return str(num)
    else:
        return "error"


if __name__ == "__main__":
    server.run(debug=True, port=8888, host="0.0.0.0")
