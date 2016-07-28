#!
from flask import Flask, request, Response
import os
from simplejson import load

"""
Copied from: https://realpython.com/blog/python/getting-started-with-the-slack-api-using-python-and-flask/
"""


app = Flask(__name__)


def __get_slack_webhook_secret():
    config_path = "{0}/config/config.private".format(os.path.dirname(os.path.realpath(__file__)))
    if not os.path.isfile(config_path):
        raise Exception("config not found at {}".format(config_path))
    with open(config_path, "r") as f:
        return load(f)["SLACK_WEBHOOK_SECRET"]


@app.route('/slack', methods=['POST'])
def inbound():
    if request.form.get('token') == __get_slack_webhook_secret():
        channel = request.form.get('channel_name')
        username = request.form.get('user_name')
        text = request.form.get('text')
        inbound_message = username + " in " + channel + " says: " + text
        print(inbound_message)
    return Response(), 200


@app.route('/', methods=['GET'])
def test():
    return Response('It works!')


if __name__ == "__main__":
    app.run(debug=True)