"""
    Bookmarky Api
    Controller Model
    Bookmark

"""
import logging

from flask import Blueprint, jsonify, Response

from bookmarky.api.controllers.models import ctrl_base
from bookmarky.api.models.bookmark import Bookmark
from bookmarky.api.models.bookmark_tag import BookmarkTag
from bookmarky.api.utils import auth
from bookmarky.api.utils import api_util
from bookmarky.api.utils import glow

ctrl_bookmark = Blueprint("bookmark", __name__, url_prefix="/bookmark")


@ctrl_bookmark.route("")
@ctrl_bookmark.route("/")
@ctrl_bookmark.route("/<bookmark_id>", methods=["GET"])
@auth.auth_request
def get_model(bookmark_id: int = None) -> Response:
    """GET operation for a bookmark.
    GET /user
    """
    logging.info("GET - /bookmark")
    data = ctrl_base.get_model(Bookmark, bookmark_id)
    if not isinstance(data, dict):
        return data
    return jsonify(data)


@ctrl_bookmark.route("", methods=["POST"])
@ctrl_bookmark.route("/", methods=["POST"])
@ctrl_bookmark.route("/<bookmark_id>", methods=["POST"])
@ctrl_bookmark.route("/<bookmark_id>/", methods=["POST"])
@auth.auth_request
def post_model(bookmark_id: int = None):
    """POST operation for a Bookmark model.
    POST /bookmark
    @todo: This needs to be locked down to only allow users to delete their own Tag relationships
    """
    data = {
        "user_id": glow.user["user_id"]
    }
    logging.info("POST Bookmark")
    r_args = api_util.get_post_data()
    if r_args and "tag_id" in r_args:
        BookmarkTag().create(bookmark_id, r_args["tag_id"])
    if r_args and "tag_id_remove" in r_args:
        BookmarkTag().remove(bookmark_id, r_args["tag_id_remove"])
    return ctrl_base.post_model(Bookmark, bookmark_id, data)


@ctrl_bookmark.route("/meta/<bookmark_id>", methods=["POST"])
@auth.auth_request
def post_model_meta(bookmark_id: int = None):
    """POST operation for a Bookmark model metas.
    POST /meta/bookmark
    @todo: This needs to be locked down to only allow users to delete their own Tag relationships
    """
    data = {
        "user_id": glow.user["user_id"]
    }
    logging.info("POST Bookmark")
    r_args = api_util.get_post_data()
    if r_args and "tag_id" in r_args:
        BookmarkTag().create(bookmark_id, r_args["tag_id"])
    if r_args and "tag_id_remove" in r_args:
        BookmarkTag().remove(bookmark_id, r_args["tag_id_remove"])
    return ctrl_base.post_model(Bookmark, bookmark_id, data)


@ctrl_bookmark.route("/<bookmark_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(bookmark_id: int = None):
    """DELETE operation for a Bookmark model.
    DELETE /bookmark
    """
    logging.debug("DELETE Bookmark")
    return ctrl_base.delete_model(Bookmark, bookmark_id)


# End File: politeauthority/bookmarky-api/src/bookmarky/api/controllers/ctrl_models/ctrl_bookmark.py
