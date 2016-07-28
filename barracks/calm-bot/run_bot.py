#!
from flask import Flask, request, Response
import os
from simplejson import load
from slackclient import SlackClient


app = Flask(__name__)


def __get_slack_creds(cred):
    config_path = "{0}/config/config.private".format(os.path.dirname(os.path.realpath(__file__)))
    if not os.path.isfile(config_path):
        raise Exception("config not found at {}".format(config_path))
    with open(config_path, "r") as f:

        config = load(f)
        if cred == "webhook":
            return config["SLACK_WEBHOOK_SECRET"]
        elif cred == "token":
            return config["SLACK_TOKEN"]
        else:
            raise Exception("Unknown credential")


def respond(channel, user_name):

    response = "┬─┬﻿ ノ( ゜-゜ノ)    Be well @{}".format(user_name)

    slack_client = SlackClient(__get_slack_creds("token"))
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response,
        username='calm-bot',
        icon_emoji=':robot_face:'
    )


@app.route('/slack', methods=['POST'])
def inbound():
    if request.form.get("token") == __get_slack_creds("webhook"):

        # get incoming channel
        channel = request.form.get("channel_id")
        user = request.form.get("user_name")

        #respond
        respond(channel, user)

    return Response(), 200


if __name__ == "__main__":
    app.run(debug=True)