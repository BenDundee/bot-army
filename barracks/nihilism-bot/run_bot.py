#!

from csv import DictReader
from flask import Flask, request, Response
import os
from random import choice
from simplejson import dumps
from slackclient import SlackClient

from barracks.util import get_slack_creds


app = Flask(__name__)
BASE_PATH = os.path.dirname(os.path.realpath(__file__))


MY_BOT_IS_CALLED = "nihilism-bot"


def respond(channel):

    with open("{}/assets/nihilist_quotes.txt".format(BASE_PATH), 'r') as f:
        reader = DictReader(f, delimiter="|")
        quotes = list(reader)
    quote = choice(quotes)

    response = {
        "text": quote["quote"],
        "attachments": [
            {
                "text": "{0}\n{1}".format(quote["author"], quote["source"])
            }
        ]
    }
    slack_client = SlackClient("xoxp-2334828949-3845128274-64329232069-800a97b447")
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        username=MY_BOT_IS_CALLED,
        icon_emoji=":nihilist_arbys:",
        **response
    )


@app.route('/slack', methods=['POST'])
def inbound():
    if request.form.get("token") == "WFoQyt5m3iwKqu9ieXZ5AaKu":

        # get incoming channel
        channel = request.form.get("channel_id")

        # respond
        respond(channel)

    return Response(), 200


if __name__ == "__main__":
    app.run(debug=True)