
import numpy as np
import pickle

from scipy.optimize import fmin_bfgs
from sklearn.cluster import KMeans

from barracks.util import get_logger

from ._data_loader import DataLoader

np.random.seed(42)  # 42 is the answer


class Recommender(object):

    def __init__(self, n_features=20):

        self.logger = get_logger(__name__)
        self.n_features = n_features

    def load(self, data):

        # restaurants with only a few ratings are heavily influencing results.  Let's drop them
        data.dropna(axis=0, thresh=5, inplace=True)

        self.data = data
        self.n_items, self.n_users = data.shape

        # do some mean subtraction
        self.means = np.nanmean(data.values, axis=1)
        self.y = data.values - np.reshape(self.means, (self.means.shape[0], 1))

    def load_pre_trained_model(self, filepath):

        with open(filepath, 'rb') as fp:
            model = pickle.load(fp)

        # let's just copy all the attributes from the loaded model into the current object. Surely that's not a bad idea
        self.__dict__.update(model.__dict__)

    def _flatten_params(self, X, Theta):

        return np.concatenate((X.flatten(), Theta.flatten()))

    def _unflatten_params(self, params):

        X = params[:self.n_items * self.n_features].reshape(self.n_items, self.n_features)
        Theta = params[self.n_items * self.n_features:].reshape(self.n_users, self.n_features)

        return X, Theta

    def _compute_cost(self, params, y, alpha):

        X, Theta = self._unflatten_params(params)

        cost = 0.5 * np.nansum((np.matmul(X, Theta.T) - y)**2) + \
                        0.5 * alpha * np.sum(X**2) + \
                        0.5 * alpha * np.sum(Theta**2)

        return cost

    def train(self):

        # initialize x, theta to small random values
        X = np.random.rand(self.n_items, self.n_features)
        Theta = np.random.rand(self.n_users, self.n_features)

        self.logger.info('Training the model')

        # build recommendation & learn weights
        res = fmin_bfgs(self._compute_cost, self._flatten_params(X, Theta), args=(self.y, .1))
        X, Theta = self._unflatten_params(res)

        self.X = X
        self.Theta = Theta

        self.logger.info('Model successfully trained.')

    def get_rating(self, user, item):

        # predict a user's recommendation for a given restaurant
        try:
            icol = self.data.columns.get_loc(user)
        except KeyError:
            raise Exception("User '{0}' is not in our database".format(user))

        try:
            irow = self.data.index.get_loc(item)
        except KeyError:
            raise Exception("Restuarant '{1}' is not in our database".format(item))

        rating = np.dot(self.Theta[icol, :], self.X[irow, :]) + self.means[irow]
        return rating

    def save_model(self, filepath):

        self.logger.info('Writing model params to {0}'.format(filepath))
        del self.logger  # for some reason, this is un-pickleable

        with open(filepath, 'wb') as fp:
            pickle.dump(self, fp)

    def find_optimal_groups(self, n_groups=4):

        km = KMeans(n_clusters=n_groups, random_state=42)
        km.fit(self.Theta)

        names = self.data.columns
        predictions = km.predict(self.Theta)

        groups = []
        for i in range(n_groups):
            group_inds = np.where(predictions == i)
            group = names[group_inds]

            groups.append(group.tolist())

        return groups

    def recommend_restuarant_for_group(self, group, n_suggestions=3):

        # given a group of people, find the restaurants they collaboratively rate the highest

        group_idx = [self.data.columns.get_loc(x) for x in group]

        # compute all predictions
        Y = np.matmul(self.X, self.Theta.T) + np.reshape(self.means, (self.means.shape[0], 1))
        # take subset containing the users in this group
        ys = Y[:, group_idx]

        combined_ratings = ys.sum(axis=1)
        top_n = np.argsort(-combined_ratings)[:n_suggestions]

        names = self.data.index[top_n].values.tolist()

        return names

if __name__ == '__main__':

    dataloader = DataLoader('/Users/jjardel/Work/bot-army/barracks/lunch-bot/data/survey_data.csv')

    data = dataloader.data

    rm = Recommender()
    rm.load(data)
    rm.train()
