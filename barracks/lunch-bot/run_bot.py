from bot import DataLoader, Recommender



if __name__ == '__main__':

    dataloader = DataLoader('/Users/jjardel/Work/bot-army/barracks/lunch-bot/data/survey_data.csv')
    dataloader.load()

    data = dataloader.data

    rm = Recommender()
    rm.load(data)
    rm.build()

    print("break")
