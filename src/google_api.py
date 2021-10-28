from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
import os
import pickle
from http import server
from googleapiclient.http import MediaFileUpload
import datetime

import oauth2client
from oauth2client import file

import sys


# https://developers.google.com/youtube/v3/docs/videos/insert

CLIENT_SECRETS_FILE = r'./client_secrets.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube"]


def get_code(authorize_url):
    """Show authorization URL and return the code the user wrote."""
    message = "Check this link in your browser: {0}".format(authorize_url)
    sys.stderr.write(message + "\n")
    try:
        input = raw_input  # For Python2 compatability
    except NameError:
        # For Python3 on Windows compatability
        try:
            from builtins import input as input
        except ImportError:
            pass
    return input("Enter verification code: ")


def _get_credentials_interactively(flow, storage, get_code_callback):
    """Return the credentials asking the user."""
    flow.redirect_uri = oauth2client.client.OOB_CALLBACK_URN
    authorize_url = flow.step1_get_authorize_url()
    code = get_code_callback(authorize_url)
    if code:
        credential = flow.step2_exchange(code, http=None)
        storage.put(credential)
        credential.set_store(storage)
        return credential


def _get_credentials(flow, storage, get_code_callback):
    """Return the user credentials. If not found, run the interactive flow."""
    existing_credentials = storage.get()
    if existing_credentials and not existing_credentials.invalid:
        return existing_credentials
    else:
        return _get_credentials_interactively(flow, storage, get_code_callback)


def Create_Service(get_code_callback):
    print(CLIENT_SECRETS_FILE, API_NAME, API_VERSION, SCOPES, sep='-')

    cred = None

    pickle_file = f'token_{API_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

        # print(f"{cred.access_token = }")
        # print(f"{cred.client_id = }")
        # print(f"{cred.client_secret = }")
        # print(f"{cred.refresh_token = }")
        # print(f"{cred.store = }")
        # print(f"{cred.token_expiry = }")
        # print(f"{cred.token_uri = }")
        # print(f"{cred.user_agent = }")
        # print(f"{cred.revoke_uri = }")
        # print(f"{cred.id_token = }")
        # print(f"{cred.id_token_jwt = }")
        # print(f"{cred.token_response = }")
        # print(f"{cred.scopes = }")
        # print(f"{cred.token_info_uri = }")

        # print(f"{cred.invalid = }")

    if not cred or cred.invalid:
        if cred and not cred.access_token_expired() and cred.refresh_token:
            cred.refresh(Request())
        else:
            get_flow = oauth2client.client.flow_from_clientsecrets
            flow = get_flow(CLIENT_SECRETS_FILE, scope=SCOPES)

            storage = file.Storage(pickle_file)
            cred = _get_credentials(flow, storage, get_code_callback)

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_NAME, API_VERSION, credentials=cred)
        print(API_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None


def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt


service = Create_Service(get_code)

body = {  # https://developers.google.com/youtube/v3/docs/videos#resource
    'snippet': {
        'categoryI': 24,
        'title': 'Best twitch clip',
        'description': 'You can found more info on this channel ....',
        'tags': ['clip', 'twitch', 'lsf', 'livestreamfails', 'fails']
    },
    'status': {
        'privacyStatus': 'private',
        'selfDeclaredMadeForKids': True
    },
    # 'recordingDetails': {
    #     'recordingDate': datetime.datetime.now().isoformat() + "Z"
    # }
}

media_file = MediaFileUpload(
    "clips/EndearingKathishRaisinPRChase-qUwoNeVyK_snNrHU.mp4")
response_upload = service.videos().insert(
    part='snippet,status',
    body=body,
    media_body=media_file
)
