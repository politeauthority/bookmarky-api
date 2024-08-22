"""
    Bookmark Api
    Controller Collection
    Bookmarks

"""

from flask import Blueprint, jsonify

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
                "op": "eq"
            }
        },
        "order_by": {},
        "limit": None
    }
    data = ctrl_collection_base.get(Bookmarks, extra_args)
    data["objects"] = Tags().get_tags_for_bookmarks(data["objects"])
    return jsonify(data)

# End File: politeauthority/bookmarky/src/bookmarky/api/controllers/collections/ctrl_bookmarks.py
