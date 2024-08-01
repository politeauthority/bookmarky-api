"""
    Bookmark Api
    Controller Collection - Tags

"""

from flask import Blueprint, jsonify

from bookmarky.api.collects.tags import Tags
from bookmarky.api.controllers.collections import ctrl_collection_base
from bookmarky.api.utils import auth

ctrl_tags = Blueprint("tags", __name__, url_prefix="/tags")


@ctrl_tags.route("")
@auth.auth_request
def index():
    """Get Tags."""
    data = ctrl_collection_base.get(Tags)
    return jsonify(data)


# End File: politeauthority/bookmarky/src/bookmarky/api/controllers/ctrl_collections/ctrl_tags.py
