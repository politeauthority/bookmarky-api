"""
    Bookmarky Api
    Controller Model
    Bookmark

"""
import logging

from flask import Blueprint, jsonify, Response

from bookmarky.api.controllers.models import ctrl_base
from bookmarky.api.models.bookmark import Bookmark
from bookmarky.api.utils import auth

ctrl_bookmark = Blueprint("bookmark", __name__, url_prefix="/bookmark")


@ctrl_bookmark.route("")
@ctrl_bookmark.route("/")
@ctrl_bookmark.route("/<bookmark_id>", methods=["GET"])
@auth.auth_request
def get_model(user_id: int = None) -> Response:
    """GET operation for a bookmark.
    GET /user
    """
    logging.info("GET - /user")
    data = ctrl_base.get_model(Bookmark, user_id)
    if not isinstance(data, dict):
        return data
    return jsonify(data)


@ctrl_bookmark.route("", methods=["POST"])
@ctrl_bookmark.route("/", methods=["POST"])
@ctrl_bookmark.route("/<user_id>", methods=["POST"])
@auth.auth_request
def post_model(bookmark_id: int = None):
    """POST operation for a User model.
    POST /bookmark
    """
    logging.info("POST User")
    return ctrl_base.post_model(Bookmark, bookmark_id)


@ctrl_bookmark.route("/<bookmark_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(bookmark_id: int = None):
    """DELETE operation for a User model.
    DELETE /bookmark
    """
    logging.debug("DELETE Bookmark")
    return ctrl_base.delete_model(Bookmark, bookmark_id)


# End File: bookmarky/src/bookmarky/api/controllers/ctrl_models/ctrl_bookmark.py
