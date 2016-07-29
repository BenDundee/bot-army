#!
from barracks.util import get_bulleted_list
from ._recommender import Recommender


def get_rating(recommender, user, restaurant):
    return recommender.get_rating(user, restaurant)


def find_optimal_groups(recommender):
    return recommender.find_optimal_groups()


def find_optimal_restaurant(recommender, users):
    try:
        return recommender.find_optimal_restaurants(users)
    except Exception:
        raise NotImplementedError("Not implemented yet")


__REGISTRY = {
    "get_rating": get_rating,
    "find_optimal_groups": find_optimal_groups,
    "find_optimal_restaurant": find_optimal_restaurant
}


def responses(call, recommender, **kwargs):
    """

    :param call: See __REGISTRY, above
    :param recommender: recommendation engine
     :type recommender: Recommender
    :param kwargs: args to pass to method
    :return:
    """
    if call not in __REGISTRY:
        raise Exception(
            "Response {0} is unsupported. Please choose one of:\n{1}"
            .format(call, get_bulleted_list(__REGISTRY.keys()))
        )
    return __REGISTRY[call](kwargs)