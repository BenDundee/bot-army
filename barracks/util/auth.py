#!
from os.path import isfile
from simplejson import load


__CONFIG_LOCATION = "../../config/config.private"


def __get_config():
    if not isfile(__CONFIG_LOCATION):
        raise Exception("config file not found at {}".format(__CONFIG_LOCATION))
    with open("../../config/config.private", "r") as f:
        return load(f.read())


def get_api_token():
    """
    Gets the API token stored in the config file. Config file must be named config.private.
    """
    config = __get_config()
    try:
        return config["SLACK_TOKEN"]
    except KeyError as e:
        raise Exception("config file did not contain correct key. see config.private.example.")


def get_webhook_secret():
    """
    Gets the webhook secret in the config file. Config file must be named config.private
    """
    config = __get_config()
    try:
        return config["SLACK_WEBHOOK_SECRET"]
    except KeyError as e:
        raise Exception("config file did not contain correct key. see config.private.example.")