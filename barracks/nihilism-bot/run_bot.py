#!

from csv import DictReader
from flask import Flask, request, Response
import os
from random import choice
from slackclient import SlackClient
from simplejson import dumps


app = Flask(__name__)
BASE_PATH = os.path.dirname(os.path.realpath(__file__))


MY_BOT_IS_CALLED = "nihilism-bot"


def respond(channel):

    with open("{}/assets/nihilist_quotes.txt".format(BASE_PATH), 'r') as f:
        reader = DictReader(f, delimiter="|")
        quotes = list(reader)
    quote = choice(quotes)
    print(quote)

    response = {
        "text": quote["quote"],
        "attachments": [
            {
                "text": "{0}\n{1}".format(quote["author"], quote["source"])
            }
        ]
    }
    slack_client = SlackClient(os.environ.get("SLACK_TOKEN"))
    print("posting message to slack on channel {}".format(channel))
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        username=MY_BOT_IS_CALLED,
        icon_emoji=":nihilist_arbys:",
        **response
    )


@app.route('/slack', methods=['POST'])
def inbound():
    if request.form.get("token") == os.environ.get("SLACK_WEBHOOK_SECRET"):

        # get incoming channel
        channel = request.form.get("channel_id")

        # respond
        respond(channel)

    return Response(), 200


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)