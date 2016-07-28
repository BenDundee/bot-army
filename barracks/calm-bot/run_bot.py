#!
# -*- coding: utf-8 -*-

from flask import Flask, request, Response
import os
from slackclient import SlackClient



def get_slack_creds(base_path):
    """
    Store config.private files in your bot's config folder--make sure they are .gitignore'd.

    Example usage: get_slack_creds(__file__)

    :param base_path:
    :return: dict[str, str]
    """
    return {
        "SLACK_TOKEN": os.environ.get("SLACK_TOKEN"),
        "SLACK_WEBHOOK_SECRET": os.environ.get("SLACK_WEBHOOK_SECRET")
    }


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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


