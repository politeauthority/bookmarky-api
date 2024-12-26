"""
    Bookmarky Api
    Controller Model
    Auto Feature

"""
import logging

from flask import Blueprint, jsonify, Response

from bookmarky.api.controllers.models import ctrl_base
from bookmarky.api.models.auto_feature import AutoFeature
from bookmarky.api.utils import auth
from bookmarky.api.utils import api_util
from bookmarky.api.utils import glow

ctrl_auto_feature = Blueprint("auto-feature", __name__, url_prefix="/auto-feature")


@ctrl_auto_feature.route("/")
@ctrl_auto_feature.route("/<af_id>", methods=["GET"])
@auth.auth_request
def get_model(af_id: int = None) -> Response:
    """GET operation for a AutoFeature.
    GET /auto-feature
    """
    logging.info("GET - /bookmark")
    data = ctrl_base.get_model(AutoFeature, af_id)
    if not isinstance(data, dict):
        return data
    return jsonify(data)


@ctrl_auto_feature.route("", methods=["POST"])
@ctrl_auto_feature.route("/", methods=["POST"])
@ctrl_auto_feature.route("/<af_id>", methods=["POST"])
@ctrl_auto_feature.route("/<af_id>/", methods=["POST"])
@auth.auth_request
def post_model(af_id: int = None):
    """POST operation for a AutoFeature model.
    POST /auto-feature
    """
    logging.info("POST Auto Feature")
    data = {
        "user_id": glow.user["user_id"]
    }
    if isinstance(af_id, str):
        try:
            af_id = int(af_id)
        except ValueError:
            return {"status": "error"}, 400
    r_args = api_util.get_post_data()
    data.update(r_args)
    response, return_code = ctrl_base.post_model(AutoFeature, af_id, data)
    if isinstance(response, Response):
        return response, return_code
    ret_data = response
    return jsonify(ret_data), return_code


@ctrl_auto_feature.route("/<af_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(af_id: int = None):
    """DELETE operation for a Auto Feature entity.
    DELETE /auto-feature
    """
    data = {
        "status": "Error",
        "message": "Could not find Auto Feature ID: %s" % af_id
    }
    logging.debug("DELETE Bookmark")
    af = AutoFeature()
    if not af.get_by_id(af_id):
        return jsonify(data), 404
    if af.user_id != glow.user["user_id"]:
        logging.warning("User %s tried to delete AutoFeature beloning to User: %s" % (
            glow.user["user_id"],
            af.user_id
        ))
        return jsonify(data), 404
    return ctrl_base.delete_model(AutoFeature, af.id)

# End File: politeauthority/bookmarky-api/src/bookmarky/api/controllers/ctrl_models/
#               ctrl_auto_feature.py
