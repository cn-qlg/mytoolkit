import json
from typing import Optional

import requests

SLACK_WEBHOOK_URL = ""
# How many seconds to give Slack API to process the request
TIMEOUT = 8
DEFAULT_USER_NAME = "Alarm"


def set_config(slack_webhook_url: str, user_name: str = DEFAULT_USER_NAME):
    global SLACK_WEBHOOK_URL, DEFAULT_USER_NAME
    SLACK_WEBHOOK_URL = slack_webhook_url
    DEFAULT_USER_NAME = user_name


class Slack:
    @staticmethod
    def escape(msg: str) -> str:
        """
        Escapes &, <, and >

        :param msg: The raw string
        :return: The escaped string
        """
        msg = msg.replace("&", "&amp;")
        msg = msg.replace("<", "&lt;")
        msg = msg.replace(">", "&gt;")
        return msg

    @classmethod
    def send(
        cls,
        msg: str,
        channel: str,
        username: Optional[str] = None,
        icon_url: Optional[str] = None,
        icon_emoji: Optional[str] = None,
        escape: bool = True,
    ) -> bool:
        """
        Send a message to Slack

        :param msg: The text to be sent
        :param channel: The channel (start with #) or user (start with @)
        :param username: The "username" posting on Slack
        :param icon_url:
        :param icon_emoji:
        :param bool escape: Escapes &, <, and >
        :return:
        """
        if not SLACK_WEBHOOK_URL:
            raise Exception("slack webbook url not set")

        if escape:
            msg = cls.escape(msg)

        if not username:
            username = DEFAULT_USER_NAME

        payload = {"text": msg, "channel": channel, "username": username}
        if icon_url:
            payload["icon_url"] = icon_url
        elif icon_emoji:
            payload["icon_emoji"] = icon_emoji

        try:
            r = requests.post(
                SLACK_WEBHOOK_URL,
                data={"payload": json.dumps(payload)},
                timeout=TIMEOUT,
            )
            r.raise_for_status()
            return True
        except Exception:
            return False
