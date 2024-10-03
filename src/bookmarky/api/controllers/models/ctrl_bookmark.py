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
from bookmarky.api.collects.bookmark_tags import BookmarkTags
from bookmarky.api.utils import auth
from bookmarky.api.utils import api_util
from bookmarky.api.utils import glow
from bookmarky.api.utils.auto_tag_features import AutoTagFeatures

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
    data, return_code = ctrl_base.post_model(Bookmark, bookmark_id, data)
    if data["status"] == "success":
        _handle_auto_features(data)
    return data, return_code


# @ctrl_bookmark.route("/meta/<bookmark_id>", methods=["POST"])
# @auth.auth_request
# def post_model_meta(bookmark_id: int = None):
#     """POST operation for a Bookmark model metas.
#     POST /meta/bookmark
#     @todo: This needs to be locked down to only allow users to delete their own Tag relationships
#     """
#     data = {
#         "user_id": glow.user["user_id"]
#     }
#     logging.info("POST Bookmark")
#     r_args = api_util.get_post_data()
#     if r_args and "tag_id" in r_args:
#         BookmarkTag().create(bookmark_id, r_args["tag_id"])
#     if r_args and "tag_id_remove" in r_args:
#         BookmarkTag().remove(bookmark_id, r_args["tag_id_remove"])
#     return ctrl_base.post_model(Bookmark, bookmark_id, data)


@ctrl_bookmark.route("/<bookmark_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(bookmark_id: int = None):
    """DELETE operation for a Bookmark model.
    DELETE /bookmark
    Dont let a user delete a Bookmark they do not own, however we will send back a 404 in that
    event.
    @todo: Move BookmarkTag deletion logic down to the Tag model level, not the controller level so
    that it works outside of just API requests and is more encompassing
    """
    data = {
        "status": "Error",
        "message": "Could not find Bookmark ID: %s" % bookmark_id
    }
    logging.debug("DELETE Bookmark")
    bookmark = Bookmark()
    if not bookmark.get_by_id(bookmark_id):
        return jsonify(data), 404
    if bookmark.user_id != glow.user["user_id"]:
        logging.warning("User %s tried to delete Bookmark beloning to User: %s" % (
            glow.user["user_id"],
            bookmark.user_id
        ))
        return jsonify(data), 404
    bts_col = BookmarkTags()
    bts_col.delete_for_bookmark(bookmark.id)
    return ctrl_base.delete_model(Bookmark, bookmark.id)


def _handle_auto_features(data: dict) -> bool:
    """When we add a Bookmark, run through all the Auto Features and apply all of those which fit
    the Bookmark.
    """
    bookmark = Bookmark()
    bookmark.build_from_dict(data["object"])
    AutoTagFeatures().run(glow.user["user_id"], bookmark)
    return True

# End File: politeauthority/bookmarky-api/src/bookmarky/api/controllers/ctrl_models/ctrl_bookmark.py
