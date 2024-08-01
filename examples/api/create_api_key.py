"""
    Examples - Api
    Create a new Api Key for a User

"""
import requests

API_URL=""
API_CLIENT_ID = "w6lk58ufsw"
API_API_KEY = "32e7-i26h-tnvm-2umq"


def run():
    get_token()


def get_token():
    data = {
        "X-Api-Key": API_API_KEY,
        "Client-Id": API_CLIENT_ID,
    }
    response = requests.post("{API_URL}/auth", data=json.dumps())


if __name__ == "__main__":
    run()

# End File: politeauthority/bookmarky/examples/create-api-key.py
