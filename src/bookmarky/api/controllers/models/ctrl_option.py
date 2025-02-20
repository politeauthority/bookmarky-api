"""
    Bookmarky Api
    Controller Model
    Option

"""
import logging

from flask import Blueprint, jsonify, Response

from bookmarky.api.controllers.models import ctrl_base
from bookmarky.api.models.option import Option
from bookmarky.api.utils import auth

ctrl_option = Blueprint("option", __name__, url_prefix="/option")


@ctrl_option.route("")
@ctrl_option.route("/")
@ctrl_option.route("/<option_id>")
@auth.auth_request
def get_model(option_id: int = None) -> Response:
    """GET operation for an Option.
    GET /option
    """
    option = ctrl_base.get_model(Option, option_id)
    if not isinstance(option, dict):
        return option
    return jsonify(option)


@ctrl_option.route("", methods=["POST"])
@ctrl_option.route("/", methods=["POST"])
@ctrl_option.route("/<option_id>", methods=["POST"])
@auth.auth_request
def post_model(option_id: int = None):
    """POST operation for an Option model.
    POST /option
    """
    logging.info("POST Option")
    return ctrl_base.post_model(Option, option_id)


# End File: bookmarky/src/bookmarky/api/controllers/ctrl_models/ctrl_option.py
