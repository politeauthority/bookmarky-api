"""
    Bookmarky Api
    Controller Model - Tag

"""
import logging

from flask import Blueprint, jsonify, Response

from bookmarky.api.controllers.models import ctrl_base
from bookmarky.api.models.tag import Tag
from bookmarky.api.utils import auth

ctrl_tag = Blueprint("tag", __name__, url_prefix="/tag")


@ctrl_tag.route("")
@ctrl_tag.route("/")
@ctrl_tag.route("/<bookmark_id>", methods=["GET"])
@auth.auth_request
def get_model(user_id: int = None) -> Response:
    """GET operation for a bookmark.
    GET /tag
    """
    logging.info("GET - /tag")
    data = ctrl_base.get_model(Tag, user_id)
    if not isinstance(data, dict):
        return data
    return jsonify(data)


@ctrl_tag.route("", methods=["POST"])
@ctrl_tag.route("/", methods=["POST"])
@ctrl_tag.route("/<user_id>", methods=["POST"])
@auth.auth_request
def post_model(tag_id: int = None):
    """POST operation for a User model.
    POST /tag
    """
    logging.info("POST Tag")
    return ctrl_base.post_model(Tag, tag_id)


@ctrl_tag.route("/<tag_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(tag_id: int = None):
    """DELETE operation for a Tag model.
    DELETE /tag
    """
    logging.debug("DELETE Bookmark")
    return ctrl_base.delete_model(Tag, tag_id)


# End File: politeauthority/bookmarky/src/bookmarky/api/controllers/ctrl_models/ctrl_tag.py