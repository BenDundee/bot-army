from .bot import Recommender
from barracks.util import get_canned_header, get_logger, get_default_root_logger, get_path

from flask import Request, Response, Flask
from slackclient import SlackClient
import os

app = Flask(__name__)
BASE_PATH = os.path.dirname(os.path.realpath(__file__))


MY_BOT_IS_CALLED = "lunch-bot"


@app.route("/slack-bot", methods=["POST"])
def incoming():

    pass


@app.route("", methods=["POST"])
def retrain_model():
    pass


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
