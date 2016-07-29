from bot import DataLoader, Recommender
#from ...util import get_canned_header, get_logger, get_default_root_logger



if __name__ == '__main__':



    dataloader = DataLoader('/Users/jjardel/Work/bot-army/barracks/lunch-bot/data/survey_data.csv')
    dataloader.load()

    data = dataloader.data

    rm = Recommender()
    rm.load(data)
    rm.train()

    print("break")
