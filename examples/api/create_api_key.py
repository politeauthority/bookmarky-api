"""
    Examples - Api
    Create a new Api Key for a User

"""
import json
import os

import requests

API_URL = os.environ.get("BOOKMARKY_URL")
API_CLIENT_ID = os.environ.get("BOOKMARKY_CLIENT_ID")
API_API_KEY = os.environ.get("BOOKMARKY_API_KEY")


def run():
    get_token()


def get_token():
    data = {
        "X-Api-Key": API_API_KEY,
        "Client-Id": API_CLIENT_ID,
    }
    response = requests.post("{API_URL}/auth", data=json.dumps(data))


if __name__ == "__main__":
    run()

# End File: politeauthority/bookmarky/examples/create-api-key.py
