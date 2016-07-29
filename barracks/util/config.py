#!
import os
from simplejson import load


def get_slack_creds(base_path):
    """
    Store config.private files in your bot's config folder--make sure they are .gitignore'd.

    Example usage: get_slack_creds(__file__)

    :param base_path:
    :return: dict[str, str]
    """
    config_path = "{0}/config/config.private".format(base_path)
    if not os.path.isfile(config_path):
        raise Exception("config not found at {}".format(config_path))
    with open(config_path, "r") as f:
        return load(f)
