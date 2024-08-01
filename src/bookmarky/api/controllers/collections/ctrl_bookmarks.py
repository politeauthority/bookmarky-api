"""
    Bookmark Api
    Controller Collection - Bookmarks

"""

from flask import Blueprint, jsonify

from bookmarky.api.collects.bookmarks import Bookmarks
from bookmarky.api.controllers.collections import ctrl_collection_base
from bookmarky.api.utils import auth

ctrl_bookmarks = Blueprint("bookmarks", __name__, url_prefix="/bookmarks")


@ctrl_bookmarks.route("")
@auth.auth_request
def index():
    """Get Bookmarks."""
    data = ctrl_collection_base.get(Bookmarks)
    return jsonify(data)


# End File: politeauthority/bookmarky/src/bookmarky/api/controllers/collections/ctrl_bookmarks.py
