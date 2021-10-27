import logging
from typing import List
import utils
import requests
import datetime

default_response = {"success": False, "status": -1, "json": None}

twitch_client = utils.get_content("twitch_client")
twitch_secret = utils.get_content("twitch_secret")

global_bearer_token = {
    "access_token": None,
    "expires_in": None,
    "token_type": None,
}

global_logins = {}


def get_bearer_token():
    params = (
        ("client_id", twitch_client),
        ("client_secret", twitch_secret),
        ("grant_type", "client_credentials"),
        ("scope", ""),
    )

    response = None
    try:
        response = requests.post(
            "https://id.twitch.tv/oauth2/token", params=params)
    except:
        logging.error("[get_bearer_token]: Couldn't authenticate")
        return False

    res = utils.format_response(response)

    if json := res["json"]:
        if "access_token" in json:
            global global_bearer_token
            global_bearer_token = json

    return res


def get_clips(broadcaster_id: int, first: int = 20, started_at: str = None) -> utils.RESPONSE_TYPE:
    if started_at is None:
        started_at = (datetime.datetime.now(
            datetime.timezone.utc) - datetime.timedelta(days=1)).astimezone().isoformat()

    headers = {
        'Authorization': f'Bearer {global_bearer_token["access_token"]}',
        'Client-Id': twitch_client,
    }

    params = (
        ('broadcaster_id', broadcaster_id),
        ('first', first),
        ("started_at", started_at)
    )

    response = None
    try:
        response = requests.get(
            'https://api.twitch.tv/helix/clips', headers=headers, params=params)
    except:
        logging.error(
            f"[get_clips]: Couldn't fetch clips for {broadcaster_id}")
        return None

    return utils.format_response(response)
