from bot import Recommender
from barracks.util import get_canned_header, get_logger, get_default_root_logger, get_path


if __name__ == '__main__':

    loc = get_path(__file__) + '{0}'
    logger = get_default_root_logger(filename=loc.format('log/log.log'))

    logger = get_canned_header(logger, 'LunchBot: Making Lunch Great Again!!!')

    rm = Recommender()
    rm.load_pre_trained_model(loc.format('data/model.pkl'))

    print("break")
