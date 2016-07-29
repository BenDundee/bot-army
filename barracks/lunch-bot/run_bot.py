from .bot import Recommender, responses
from barracks.util import get_canned_header, get_logger, get_default_root_logger, get_path

from flask import request, Response, Flask
from slackclient import SlackClient
import os

app = Flask(__name__)
BASE_PATH = os.path.dirname(os.path.realpath(__file__))


MY_BOT_IS_CALLED = "lunch-bot"


def return_help():
    return {
        "text": "lunch-bot did not understand you. lunch-bot accepts the following requests:",
        "attachments": [
            {"text": "Returns your ratings for a restaurant: lunch-bot ratings <restaurant_name>"},
            {"text": "Returns optimal lunch groups: lunch-bot find optimal groups"},
            {
                "text": "Returns suggestions for a group (includes requesting user): "
                        "lunch-bot find restaurant @user1 @user2 ..."
            }
        ]
    }


def parse_message(msg, user):

    bits = msg.split(' ')
    # Assume: lunch-bot rating <restaurant_name>
    if bits[1] == 'rating':
        out = responses("get_rating", recommender=rm, user=user, restaurant=' '.join(bits[2:]))

    # Assume: lunch-bot find optimal groups
    elif bits[1] == "find" and bits[2] == "optimal":
        out = responses("find_optimal_groups", rm)

    # Assume: lunch-bot find restaurant @user1 @user2 @user3
    elif bits[1] == "find" and bits[2] == "restaurant":
        users = [x.strip('@') for x in bits[2:]]
        users.append(user)
        out = responses("find_restaurant", rm, users)

    else:
        out = return_help()

    return out


@app.route("/slack-bot", methods=["POST"])
def router():

    _logger = get_logger(__name__)
    if request.form.get("token") == os.environ.get("SLACK_TOKEN"):

        # Get info from incoming request
        channel_id = request.form.get("channel_id")
        user = request.form.get("user_name")
        message = request.form.get("text")
        _logger.info("Incoming message from {0} on {1}: {2}".format(channel_id, user, message))

        # Parse and route
        response = parse_message(message)
        slack_client = SlackClient(os.environ.get("SLACK_TOKEN"))
        slack_client.api_call(
            "chat.postMessage",
            channel=channel_id,
            username='lunch-bot',
            icon_emoji=':sausage:',
            **response
        )

    return Response(), 200


@app.route("/model/train", methods=["POST"])
def retrain_model():
    pass


@app.route("/", methods=["GET"])
def welcome():
    return Response("Welcome to LunchBot! All your lunch are belong to us!"), 200


if __name__ == '__main__':

    loc = get_path(__file__) + '{0}'
    logger = get_default_root_logger(filename=loc.format('log/log.log'))

    logger = get_canned_header(logger, 'LunchBot: Making Lunch Great Again!!!')

    rm = Recommender()

    logger.info("Loading pre-trained model")
    rm.load_pre_trained_model(loc.format('data/model.pkl'))

    logger.info("Running app...")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
