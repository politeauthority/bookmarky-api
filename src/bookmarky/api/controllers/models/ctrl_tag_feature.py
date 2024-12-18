"""
    Bookmarky Api
    Controller Model
    Tag Feature

"""
import logging

from flask import Blueprint, jsonify, Response

from bookmarky.api.controllers.models import ctrl_base
from bookmarky.api.models.tag import Tag
# from bookmarky.api.collects.bookmark_tags import BookmarkTags
from bookmarky.api.utils import auth
# from bookmarky.api.utils import glow
# from bookmarky.api.utils import api_util
# from bookmarky.shared.utils import xlate

ctrl_tag_feature = Blueprint("tag-feature", __name__, url_prefix="/tag-feature")


@ctrl_tag_feature.route("")
@ctrl_tag_feature.route("/")
@ctrl_tag_feature.route("/<tag_search>", methods=["GET"])
@auth.auth_request
def get_model(tag_search: int = None) -> Response:
    """GET operation for a TagFeature.
    GET /tag-feature
    """
    logging.info("GET - /tag-feature")
    if tag_search:
        if tag_search.isdigit():
            tag_id = int(tag_search)
            data = ctrl_base.get_model(Tag, tag_id)
        else:
            # tag_slug = tag_search
            logging.error("we dont know what we're doing here")
            return jsonify({}), 400

    if not isinstance(data, dict):
        return data
    return jsonify(data)


# @ctrl_tag_feature.route("", methods=["POST"])
# @ctrl_tag_feature.route("/", methods=["POST"])
# @ctrl_tag_feature.route("/<tag_id>", methods=["POST"])
# @auth.auth_request
# def post_model(tag_id: int = None):
#     """POST operation for a User model.
#     POST /tag
#     """
#     logging.info("POST Tag")
#     data = {
#         "user_id": glow.user["user_id"]
#     }
#     request_args = api_util.get_params()
#     if "slug" not in request_args["raw_args"] and "name" in request_args["raw_args"]:
#         data["slug"] = xlate.slugify(request_args["raw_args"]["name"])
#     return ctrl_base.post_model(Tag, tag_id, data)


# @ctrl_tag_feature.route("/<tag_id>", methods=["DELETE"])
# @auth.auth_request
# def delete_model(tag_id: int = None):
#     """DELETE operation for a Tag model.
#     DELETE /tag
#     Dont let a user delete a Tag they do not own, however we will send back a 404 in that
#     event.
#     @todo: Move BookmarkTag deletion logic down to the Tag model level, not the controller level so
#     that it works outside of just API requests and is more encompassing
#     - Delete the tag
#     - Delete the Bookmark Tags associations
#     """
#     data = {
#         "status": "Error",
#         "message": "Could not find Tag ID: %s" % tag_id
#     }
#     logging.debug("DELETE Tag")
#     tag = Tag()
#     if not tag.get_by_id(tag_id):
#         return jsonify(data), 404
#     if tag.user_id != glow.user["user_id"]:
#         logging.warning("User %s tried to delete Bookmark beloning to User: %s" % (
#             glow.user["user_id"],
#             tag.user_id
#         ))
#         return jsonify(data), 404
#     bts_col = BookmarkTags()
#     bts_col.delete_for_tag(tag.id)
#     return ctrl_base.delete_model(Tag, tag_id)


# End File: politeauthority/bookmarky/src/bookmarky/api/controllers/ctrl_models/ctrl_tag_feature.py
