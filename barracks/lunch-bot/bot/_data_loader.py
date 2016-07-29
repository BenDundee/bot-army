import pandas as pd

class DataLoader(object):

    def __init__(self, filepath):

        self.filepath = filepath

    def load(self):
        data = pd.read_csv(self.filepath, skiprows=5)

        self.data = data

if __name__ == '__main__':

    dl = DataLoader('/Users/jjardel/Work/bot-army/barracks/lunch-bot/data/survey_data.csv')
    print('break')
