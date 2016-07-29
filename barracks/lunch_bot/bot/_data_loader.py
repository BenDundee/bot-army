import pandas as pd
from util import get_logger


class DataLoader(object):

    def __init__(self, filepath):

        self.logger = get_logger(__name__)

        self.filepath = filepath
        self.load()

    def load(self):
        data = pd.read_csv(self.filepath, skiprows=5)
        data.set_index('Restaurant', inplace=True)

        self.data = data

        self.logger.info('Data successfully loaded')


if __name__ == '__main__':

    dl = DataLoader('/Users/jjardel/Work/bot-army/barracks/lunch-bot/data/survey_data.csv')
