#!
import os

from barracks.util import get_slack_creds
from flask import Flask, request, Response
from slackclient import SlackClient

app = Flask(__name__)
BASE_PATH = os.path.dirname(os.path.realpath(__file__))


MY_BOT_IS_CALLED = "give your bot a name"


def respond(channel, user_name):

    response = "What should your bot respond?"
    slack_client = SlackClient(get_slack_creds(BASE_PATH)["SLACK_TOKEN"])
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response,
        username=MY_BOT_IS_CALLED,
        icon_emoji=":robot_face:"
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