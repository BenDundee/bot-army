#!
from util  import get_bulleted_list

from ._recommender import Recommender


def get_rating(recommender, user, restaurant):
    result = recommender.get_rating(user, restaurant)
    return {
        "text": "@{user}: lunch-bot believes your rating of {restaurant} would be {rating:.1f}-star restaurant."\
        .format(user=user, restaurant=restaurant, rating=result)
    }


def find_optimal_groups(recommender):
    result = recommender.find_optimal_groups()
    return {
        "text": "The following groups are optimal:",
        "attachments": [{"text": ", ".join(r)} for r in result]
    }


def find_optimal_restaurant(recommender, users):
    result = recommender.recommend_restaurant_for_group(users)
    return{
        "text": "The following three restaurants are all highly recommended! Please vote!",
        "attachments": [{"text": r} for r in result]
    }


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
    if kwargs:
        return __REGISTRY[call](recommender, **kwargs)
    else:
        return __REGISTRY[call](recommender)