"""
    Bookmarky Api
    Controller Model
    Bookmark Tag

"""
import logging

from flask import Blueprint, jsonify, Response

from bookmarky.api.controllers.models import ctrl_base
from bookmarky.api.models.bookmark_tag import BookmarkTag
from bookmarky.api.utils import auth
from bookmarky.api.utils import glow

ctrl_bookmark_tag = Blueprint("bookmark-tag", __name__, url_prefix="/bookmark-tag")


@ctrl_bookmark_tag.route("")
@ctrl_bookmark_tag.route("/")
@ctrl_bookmark_tag.route("/<bookmark_tag_id>", methods=["GET"])
@auth.auth_request
def get_model(bookmark_tag_id: int = None) -> Response:
    """GET operation for a bookmark.
    GET /user
    """
    logging.info("GET - /bookmark")
    data = ctrl_base.get_model(BookmarkTag, bookmark_tag_id)
    if not isinstance(data, dict):
        return data
    return jsonify(data)


@ctrl_bookmark_tag.route("", methods=["POST"])
@ctrl_bookmark_tag.route("/", methods=["POST"])
@ctrl_bookmark_tag.route("/<bookmark_tag_id>", methods=["POST"])
@auth.auth_request
def post_model(bookmark_tag_id: int = None):
    """POST operation for a User model.
    POST /bookmark
    """
    data = {
        "user_id": glow.user["user_id"]
    }
    logging.info("POST Bookmark")
    return ctrl_base.post_model(BookmarkTag, bookmark_tag_id, data)


@ctrl_bookmark_tag.route("/<bookmark_tag_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(bookmark_tag_id: int = None):
    """DELETE operation for a Bookmark model.
    DELETE /bookmark
    """
    logging.debug("DELETE Bookmark")
    return ctrl_base.delete_model(BookmarkTag, bookmark_tag_id)


# End File: politeauthority/bookmarky-api/src/bookmarky/api/controllers/ctrl_models/
#           ctrl_bookmark_tag.py
