"""
    Examples - Api
    Get Bookmarks

"""
import argparse
import os

import requests
from rich.console import Console
# from rich.table import Table

USER_ID = 1

THE_ENV = "STAGE"
# THE_ENV = "DEV"

API_URL = os.environ.get(f"{THE_ENV}_BOOKMARKY_API_URL")
API_CLIENT_ID = os.environ.get(f"{THE_ENV}_BOOKMARKY_CLIENT_ID")
API_API_KEY = os.environ.get(f"{THE_ENV}_BOOKMARKY_API_KEY")

console = Console()


class GetBookmarks:

    def __init__(self, the_args):
        self.args = the_args
        self.token = ""
        self.set_env(self.args.env)

    def set_env(self, env_name: str) -> bool:
        self.api_url = os.environ.get(f"{env_name}_BOOKMARKY_API_URL")
        self.api_client_id = os.environ.get(f"{env_name}_BOOKMARKY_CLIENT_ID")
        self.api_key = os.environ.get(f"{env_name}_BOOKMARKY_API_KEY")
        return True

    def run(self) -> bool:
        print("Using %s on %s" % (THE_ENV, API_URL))
        token = self.get_token()
        if not token:
            print("Error: exitings")
            exit(1)
        bookmarks = self.get_bookmarks()
        if not bookmarks:
            print("Failed to get Bookmarks")
            exit(1)

    def get_token(self) -> bool:
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
        self.token = response_json["token"]
        return True

    def get_bookmarks(self) -> bool:
        headers = {
            "Token": self.token,
            "Content-Type": "application/json"
        }
        data = {
            "user_id": USER_ID,
        }
        # data.update(the_args)
        response = requests.get(
            f"{API_URL}/bookmarks",
            headers=headers,
            params=data,
            verify=False
        )
        if response.status_code not in [200, 201]:
            print("Error: could get write bookmarks. %s" % response.text)
            return False
        response_json = response.json()
        print("Got  Bookmarks:")
        for bookmark in response_json["objects"]:
            print("\t%s" % bookmark["name"])
            print("\t\t%s" % bookmark["url"])
        return True


def parse_args():
    """Parse the CLI arguments."""
    parser = argparse.ArgumentParser(description="Bookmarky Cli")
    parser.add_argument(
        "page",
        nargs='?',
        default=None,
        help='Item selector (name or id)')
    parser.add_argument('-p', '--page', default=None)
    parser.add_argument(
        "filter",
        nargs='?',
        default=None,
        help='Allows filtering of results')
    parser.add_argument('-e', '--env', default=None)
    # parser.add_argument('-f', '--filter', default=None)
    # parser.add_argument(
    #     "o",
    #     nargs='?',
    #     default=None,
    #     help="Output")
    # parser.add_argument('-o', '--output', default=None)
    # parser.add_argument('--order', default=None)
    # parser.add_argument('--delete-token', default=None)
    the_args = parser.parse_args()
    return the_args


if __name__ == "__main__":
    the_args = parse_args()
    GetBookmarks(the_args).run()

# End File: politeauthority/bookmarky/examples/get-bookmarks.py
