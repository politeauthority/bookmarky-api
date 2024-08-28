"""
    Bookmark Api
    Controller Collection
    Bookmarks

"""
import logging

from flask import Blueprint, jsonify, request

from bookmarky.api.collects.bookmarks import Bookmarks
from bookmarky.api.collects.tags import Tags
from bookmarky.api.controllers.collections import ctrl_collection_base
from bookmarky.api.utils import auth
from bookmarky.api.utils import glow


ctrl_bookmarks = Blueprint("bookmarks", __name__, url_prefix="/bookmarks")


@ctrl_bookmarks.route("")
@auth.auth_request
def index():
    """Get Bookmarks, along with associated Tags where they exist."""
    extra_args = {
        "fields": {
            "user_id": {
                "value": glow.user["user_id"],
                "op": "=",
                "overrideable": False
            }
        },
        "order_by": {},
        "limit": None
    }
    data = ctrl_collection_base.get(Bookmarks, extra_args)
    data["objects"] = Tags().get_tags_for_bookmarks(data["objects"])
    return jsonify(data)


@ctrl_bookmarks.route("/search")
@auth.auth_request
def search():
    """Get Bookmarks from a wide variety of input.
    """
    extra_args = {
        "fields": {},
        "order_by": {},
        "limit": None
    }

    search_args = request.args
    if "title" in search_args:
        extra_args["fields"]["title"] = {
            "value": glow.user["user_id"],
            "op": "LIKE",
        }
    logging.debug("\n\nBOOKMARK SEARCH\n")
    logging.debug(extra_args)
    logging.debug("\nEND SEARCH\n\n")
    data = ctrl_collection_base.get(Bookmarks, extra_args)
    data["objects"] = Tags().get_tags_for_bookmarks(data["objects"])
    return jsonify(data)

# End File: politeauthority/bookmarky-api/src/bookmarky/api/controllers/collections/
#           ctrl_bookmarks.py
