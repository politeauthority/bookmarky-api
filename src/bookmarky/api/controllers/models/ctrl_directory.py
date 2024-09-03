"""
    Bookmarky Api
    Controller Model
    Directory

"""

import logging

from flask import Blueprint, jsonify, Response

from bookmarky.api.controllers.models import ctrl_base
from bookmarky.api.models.directory import Directory
from bookmarky.api.utils import auth
from bookmarky.api.utils import api_util
from bookmarky.api.utils import glow
from bookmarky.shared.utils import xlate

ctrl_directory = Blueprint("directory", __name__, url_prefix="/directory")


@ctrl_directory.route("")
@ctrl_directory.route("/")
@ctrl_directory.route("/<dir_id>", methods=["GET"])
@auth.auth_request
def get_model(dir_id: int = None) -> Response:
    """GET operation for a Directory.
    GET /directory
    """
    logging.info("GET - /bookmark")
    data = ctrl_base.get_model(Directory, dir_id)
    if not isinstance(data, dict):
        return data
    return jsonify(data)


@ctrl_directory.route("", methods=["POST"])
@ctrl_directory.route("/", methods=["POST"])
@ctrl_directory.route("/<dir_id>", methods=["POST"])
@auth.auth_request
def post_model(dir_id: int = None):
    """POST operation for a Directory model.
    Make sure that we create a slug value from the name.
    POST /directory
    """
    dir_name = api_util.get_param("name")
    slug = None
    if dir_name:
        slug = xlate.slugify(dir_name)
    data = {
        "user_id": glow.user["user_id"],
        "slug": slug
    }
    logging.info("POST Directory")
    return ctrl_base.post_model(model=Directory, entity_id=dir_id, generated_data=data)


@ctrl_directory.route("/<dir_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(dir_id: int = None):
    """DELETE operation for a Directory model.
    DELETE /directory
    """
    logging.debug("DELETE Directory")
    return ctrl_base.delete_model(Directory, dir_id)


# End File: politeauthority/bookmarky-api/src/bookmarky/api/controllers/ctrl_models/
#           ctrl_directory.py
