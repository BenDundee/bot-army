from bot import Recommender
from barracks.util import get_canned_header, get_logger, get_default_root_logger, get_path

from flask import Request, Response, Flask
from slackclient import SlackClient
import os

app = Flask(__name__)
BASE_PATH = os.path.dirname(os.path.realpath(__file__))


MY_BOT_IS_CALLED = "lunch-bot"

if __name__ == '__main__':

    loc = get_path(__file__) + '{0}'
    logger = get_default_root_logger(filename=loc.format('log/log.log'))

    logger = get_canned_header(logger, 'LunchBot: Making Lunch Great Again!!!')

    rm = Recommender()
    rm.load_pre_trained_model(loc.format('data/model.pkl'))
    rm.recommend_restuarant_for_group(['jjardel', 'staylor', 'chris'])

    app.run(debug=True)

    print("break")
