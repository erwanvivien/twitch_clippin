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


def get_users(logins: List[str] = None):
    if not logins:
        return default_response.copy()

    global global_logins

    for l in enumerate(logins):
        if l in global_logins:
            global_logins.remove(l)

    headers = {
        'Authorization': f'Bearer {global_bearer_token["access_token"]}',
        'Client-Id': twitch_client,
    }

    all_good = True

    step = 100
    for i in range(0, len(logins), step):
        chunk = logins[i:i + step]

        params = []
        for c in chunk:
            params.append(("login", c))

        response = None
        try:
            response = requests.get(
                "https://api.twitch.tv/helix/users", params=params, headers=headers)
        except:
            logging.error("[get_users]: Couldn't retrieve users")
            all_good = False
            continue

        try:
            data = response.json()["data"]
            for i, user in enumerate(data):
                user.pop('offline_image_url', None)
                global_logins[chunk[i]] = user
        except:
            logging.error("[get_users]: Request bad formated")
            all_good = False
            continue

    return {"success": all_good, "status": 200 if all_good else -1, "json": None}
