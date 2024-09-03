"""
    Examples - Api
    Create a new Api Key for a User

    @todo: Make this better, include expiration flags

"""
import json
import os

import requests

USER_ID = 1
# THE_ENV = "STAGE
# THE_ENV = "DEV"
THE_ENV = "PROD"

API_URL = os.environ.get(f"{THE_ENV}_BOOKMARKY_API_URL")
API_CLIENT_ID = os.environ.get(f"{THE_ENV}_BOOKMARKY_CLIENT_ID")
API_API_KEY = os.environ.get(f"{THE_ENV}_BOOKMARKY_API_KEY")


def run():
    """Primary entrpoint for the create_api_key script."""
    print("Using %s on %s" % (THE_ENV, API_URL))
    token = get_token()
    if not token:
        print("Error: exitings")
        exit(1)
    create_api_key(token)


def create_api_key(token: str) -> bool:
    """Create an Api Key for the understood user."""
    headers = {
        "Token": token,
        "Content-Type": "application/json"
    }
    data = {
        "user_id": USER_ID,
    }
    response = requests.post(
        f"{API_URL}/api-key",
        headers=headers,
        data=json.dumps(data),
        verify=False
    )
    if response.status_code not in [200, 201]:
        print("Error: could not write Api Key. %s" % response.text)

        return False
    response_json = response.json()
    print("Created Api Key")
    print("\tClient Id: %s" % response_json["object"]["client_id"])
    print("\tApi Key: %s" % response_json["object"]["key"])
    return True


def get_token() -> str:
    """Get a token to use against the api."""
    headers = {
        "X-Api-Key": API_API_KEY,
        "Client-Id": API_CLIENT_ID,
    }
    response = requests.post(
        f"{API_URL}/auth",
        headers=headers,
        verify=False
    )
    if response.status_code != 200:
        print("Error: Could not get token from api. %s" % response.text)
        return False
    response_json = response.json()
    print("Aquired token!")
    return response_json["token"]


if __name__ == "__main__":
    run()

# End File: politeauthority/bookmarky/examples/create-api-key.py
