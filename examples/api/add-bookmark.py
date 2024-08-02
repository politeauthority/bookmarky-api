"""
    Examples - Api
    Add a Bookmark

"""
import json
import os

import requests

USER_ID = 1

# THE_ENV = "STAGE
THE_ENV = "DEV"

API_URL = os.environ.get(f"{THE_ENV}_BOOKMARKY_API_URL")
API_CLIENT_ID = os.environ.get(f"{THE_ENV}_BOOKMARKY_CLIENT_ID")
API_API_KEY = os.environ.get(f"{THE_ENV}_BOOKMARKY_API_KEY")


def run() -> bool:
    print("Using %s on %s" % (THE_ENV, API_URL))
    token = get_token()
    if not token:
        print("Error: exitings")
        exit(1)
    the_args = {
        "url": "https://google.com/",
        "name": "Google"
    }
    write_bookmark = create_bookmark(token, the_args)
    if write_bookmark:
        print("Wrote Bookmark")
        return True
    else:
        print("Failed to write Bookmark")
        exit(1)
        return False


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


def create_bookmark(token: str, the_args: dict) -> bool:
    headers = {
        "Token": token,
        "Content-Type": "application/json"
    }
    data = {
        "user_id": USER_ID,
    }
    data.update(the_args)
    response = requests.post(
        f"{API_URL}/bookmark",
        headers=headers,
        data=json.dumps(data),
        verify=False
    )
    if response.status_code not in [200, 201]:
        print("Error: could not write bookmark. %s" % response.text)
        return False
    response_json = response.json()
    print("Created Bookmark:")
    print(response)
    print(response_json)
    return True


if __name__ == "__main__":
    run()

# End File: politeauthority/bookmarky/examples/add-bookmark.py
