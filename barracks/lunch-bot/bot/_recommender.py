
import numpy as np
from scipy.optimize import fmin_bfgs

np.random.seed(42)  # 42 is the answer


class Recommender(object):

    def __init__(self, n_features=25):

        self.n_features = n_features

    def load(self, data):

        self.data = data
        self.n_items, self.n_users = data.shape

        # do some mean subtraction
        self.means = np.nanmean(data.values, axis=1)
        self.y = data.values - np.reshape(self.means, (self.means.shape[0], 1))


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

    def build(self):

        # initialize x, theta to small random values
        X = np.random.rand(self.n_items, self.n_features)
        Theta = np.random.rand(self.n_users, self.n_features)

        # build recommendation & learn weights
        res = fmin_bfgs(self._compute_cost, self._flatten_params(X, Theta), args=(self.y, 1.))
        X, Theta = self._unflatten_params(res)

        self.X = X
        self.Theta = Theta

    def recommend(self, user, item):

        # predict a user's recommendation for a given restaurant
        icol = self.data.columns.get_loc(user)
        irow = self.data.index.get_loc(item)

        recommendation = np.dot(self.Theta[icol, :], self.X[irow, :]) + self.means[irow]
        return recommendation


if __name__ == '__main__':

    dataloader = DataLoader('/Users/jjardel/Work/bot-army/barracks/lunch-bot/data/survey_data.csv')
    dataloader.load()

    data = dataloader.data

    rm = Recommender()
    rm.load(data)
    rm.build()
