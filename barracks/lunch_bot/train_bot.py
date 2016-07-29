from barracks.util import get_canned_header, get_default_root_logger, get_path

from .bot import DataLoader, Recommender

# call train_bot.py if you need to train the model.
# Save the trained results to disk so run_bot.py can simply load the model.


if __name__ == '__main__':

    loc = get_path(__file__) + '{0}'
    logger = get_default_root_logger(filename=loc.format('log/log.log'))

    logger = get_canned_header(logger, 'Training LunchBot')

    dl = DataLoader(loc.format('assets/survey_data.csv'))

    # load and train recommender
    recommender = Recommender()
    recommender.load(dl.data)
    recommender.train()

    recommender.save_model(loc.format('assets/model.pkl'))





