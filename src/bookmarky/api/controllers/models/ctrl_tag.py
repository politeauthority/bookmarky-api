"""
    Bookmarky Api
    Controller Model - Tag

"""
import logging

from flask import Blueprint, jsonify, Response, request

from bookmarky.api.controllers.models import ctrl_base
from bookmarky.api.models.tag import Tag
from bookmarky.api.utils import auth
from bookmarky.api.utils import glow
from bookmarky.api.utils import api_util
from bookmarky.shared.utils import xlate

ctrl_tag = Blueprint("tag", __name__, url_prefix="/tag")


@ctrl_tag.route("")
@ctrl_tag.route("/")
@ctrl_tag.route("/<tag_search>", methods=["GET"])
@auth.auth_request
def get_model(tag_search: int = None) -> Response:
    """GET operation for a bookmark.
    GET /tag
    """
    logging.info("GET - /tag")
    if tag_search:
        if tag_search.isdigit():
            tag_id = int(tag_search)
            data = ctrl_base.get_model(Tag, tag_id)
        else:
            tag_slug = tag_search
            logging.error("we dont know what we're doing here")

    if not isinstance(data, dict):
        return data
    return jsonify(data)


@ctrl_tag.route("", methods=["POST"])
@ctrl_tag.route("/", methods=["POST"])
@ctrl_tag.route("/<tag_id>", methods=["POST"])
@auth.auth_request
def post_model(tag_id: int = None):
    """POST operation for a User model.
    POST /tag
    """
    logging.info("POST Tag")
    data = {
        "user_id": glow.user["user_id"]
    }
    request_args = api_util.get_params()
    if "slug" not in request_args["raw_args"] and "name" in request_args["raw_args"]:
        data["slug"] = xlate.slugify(request_args["raw_args"]["name"])
    return ctrl_base.post_model(Tag, tag_id, data)


@ctrl_tag.route("/<tag_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(tag_id: int = None):
    """DELETE operation for a Tag model.
    DELETE /tag
    """
    logging.debug("DELETE Bookmark")
    return ctrl_base.delete_model(Tag, tag_id)


# End File: politeauthority/bookmarky/src/bookmarky/api/controllers/ctrl_models/ctrl_tag.py
