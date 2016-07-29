#!

from argparse import ArgumentParser
import os
from shutil import copytree


BOT_LANGUAGES = [
    "python",
    # "ruby",
    # "javascript"
]
TEMPLATE_LOCATIONS = {
    "python": "templates/python-bot",
}


def main(name, token="", secret="", language=""):

    if not token:
        token = input(
            "Please input your API token. Example: xoxp-0123456789-9876543210-0123456789-00000000a0\n"
        )
    if not secret:
        secret = input(
            "Please input your webhook secret. Example: AgbUUl5iRzPPo3mMnbH9o4Cu\n"
        )
    if not language:
        language = input(
            "In which language do you want to write your bot?\n"
            "The choices are: {}\n".format(','.join(BOT_LANGUAGES))
        )
        if language not in BOT_LANGUAGES:
            raise Exception(
                "Invalid language choice! Please choose from {}. (Hint: cut and paste.)"
                    .format(','.join(BOT_LANGUAGES))
            )

    # Get base directory, all paths relative to this one (should be at top level)
    base_dir = os.path.abspath(os.path.dirname(__file__)) + "/{}"

    # Create new bot
    template_location = base_dir.format(TEMPLATE_LOCATIONS[language])
    bot_location = base_dir.format("barracks/{}".format(name))
    copytree(src=template_location, dst=bot_location)

    # Create un-versioned setup script
    setup_script_name = base_dir.format("barracks/{}/bin/env_setup.sh".format(name))
    with open(setup_script_name, 'w') as f:
        f.write(
            ("#!\n\nheroku config:set SLACK_TOKEN={token}\n" +
            "heroku config:set SLACK_WEBHOOK_SECRET={secret}")
            .format(token=token, secret=secret)
        )


if __name__ == "__main__":

    parser = ArgumentParser(description="Build-a-Bot? Build-a-Bot!")
    parser.add_argument(
        "--name", type=str, help="The name for your bot",
        metavar="my-first-bot"
    )
    parser.add_argument(
        "--token", type=str,
        help="Slack API Token, should be groups of 10 numbers separated by dashes",
        metavar="xoxp-0123456789-9876543210-0123456789-00000000a0"
    )
    parser.add_argument(
        "--webhook-secret", type=str, dest="secret",
        help="Slack webhook secret, 24 mixed-case alpha-numeric characters",
        metavar="AgbUUl5iRzPPo3mMnbH9o4Cu"
    )
    parser.add_argument(
        "--lang", type=str, choices=BOT_LANGUAGES,
        help="Language in which you will write your bot"
    )

    args = parser.parse_args()
    main(
        name=args.name,
        secret=args.secret,
        token=args.token,
        language=args.lang
    )