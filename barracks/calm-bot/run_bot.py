#!
from flask import Flask, request, Response
import os
from slackclient import SlackClient

from barracks.util import get_slack_creds


app = Flask(__name__)
BASE_PATH = os.path.dirname(os.path.realpath(__file__))


def respond(channel, user_name):

    response = "┬─┬﻿ ノ( ゜-゜ノ)    Be well @{}".format(user_name)
    slack_client = SlackClient(get_slack_creds(BASE_PATH)["SLACK_TOKEN"])
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response,
        username='calm-bot',
        icon_emoji=':robot_face:'
    )


@app.route('/slack', methods=['POST'])
def inbound():
    if request.form.get("token") == get_slack_creds(BASE_PATH)["SLACK_WEBHOOK_SECRET"]:

        # get incoming channel
        channel = request.form.get("channel_id")
        user = request.form.get("user_name")

        # respond
        respond(channel, user)

    return Response(), 200


if __name__ == "__main__":
    app.run(debug=True)