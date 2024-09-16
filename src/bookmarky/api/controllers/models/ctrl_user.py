"""
    Bookmarky Api
    Controller Model
    User

"""
import logging

from flask import Blueprint, jsonify, Response

from bookmarky.api.utils import glow
from bookmarky.api.controllers.models import ctrl_base
from bookmarky.api.models.user import User
from bookmarky.api.utils import auth
from bookmarky.api.utils import api_util

ctrl_user = Blueprint("user", __name__, url_prefix="/user")


@ctrl_user.route("")
@ctrl_user.route("/")
@ctrl_user.route("/<user_id>", methods=["GET"])
@auth.auth_request
def get_model(user_id: int = None) -> Response:
    """GET operation for a User.
    GET /user
    """
    logging.info("GET - /user")
    data = ctrl_base.get_model(User, user_id)
    if not isinstance(data, dict):
        return data
    return jsonify(data)


@ctrl_user.route("", methods=["POST"])
@ctrl_user.route("/", methods=["POST"])
@ctrl_user.route("/<user_id>", methods=["POST"])
@auth.auth_request
def post_model(user_id: int = None):
    """POST operation for a User model.
    POST /role
    """
    logging.info("POST User")
    return ctrl_base.post_model(User, user_id)


@ctrl_user.route("/meta", methods=["POST"])
@auth.auth_request
def post_model_meta():
    """POST operation for a Bookmark model metas.
    POST /user/meta
    @todo: This needs to be locked down to only allow users to delete their own Tag relationships
    @todo: Create a generic version of this for ctrl_base
    """
    logging.info("POST user/meta")
    data = {
        "message": "",
        "status": "Error"
    }
    r_args = api_util.get_params()

    if "metas" not in r_args["raw_args"]:
        data["message"] = "Bad Request"
        return jsonify(data), 400

    # Check the meta fields and get ready to set them to the user
    user = User()
    metas_to_set = {}
    for meta_name, meta_field in user.field_map_metas.items():
        if meta_name in r_args["raw_args"]["metas"]:
            metas_to_set[meta_name] = r_args["raw_args"]["metas"][meta_name]

    user.get_by_id(glow.user["user_id"])
    for meta_key, meta_value in metas_to_set.items():
        user.metas[meta_key] = meta_value

    if not user.save():
        logging.error("Failed to save User")
        data["message"] = "Error saving User"
        return jsonify(data), 500
    user.load_meta()
    data["object"] = user.json()
    return jsonify(data)


@ctrl_user.route("/<user_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(user_id: int = None):
    """DELETE operation for a User model.
    DELETE /user
    """
    logging.debug("DELETE User")
    return ctrl_base.delete_model(User, user_id)


# End File: bookmarky/src/bookmarky/api/controllers/ctrl_models/ctrl_user.py
