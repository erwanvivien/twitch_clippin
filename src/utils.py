import json
import logging
import requests


RESPONSE_TYPE = type({
    "success": True,
    "status": 0,
    "json": {}
})


def get_content(file: str) -> str:
    """Gets the content of a file
    Arguments:
        file {str} -- Function name
    Returns:
        [str] -- The content of the file, as is
    """

    try:
        file = open(file, "r")
        s = file.read()
        file.close()
    except Exception as error:
        logging.error("[get_content]: Couldn't read file")
        return ""

    return s


def format_response(response: requests.Response):
    json = None
    try:
        json = response.json()
    except:
        logging.info("[format_response]: json was not valid")

    # Returns true if status_code is 2xx
    return {
        "success": response.status_code // 100 == 2,
        "status": response.status_code,
        "json": json
    }
