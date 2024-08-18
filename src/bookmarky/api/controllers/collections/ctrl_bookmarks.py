"""
    Bookmark Api
    Controller Collection
    Bookmarks

"""

from flask import Blueprint, jsonify

from bookmarky.api.collects.bookmarks import Bookmarks
# from bookmarky.api.collects.tags import Tags
from bookmarky.api.controllers.collections import ctrl_collection_base
from bookmarky.api.utils import auth
# from bookmarky.api.utils import glow


ctrl_bookmarks = Blueprint("bookmarks", __name__, url_prefix="/bookmarks")


@ctrl_bookmarks.route("")
@auth.auth_request
def index():
    """Get Bookmarks."""
    # request_args = request.args
    # extra_args = {
    #     "fields": {},
    #     "order_by": {},
    #     "limit": None
    # }
    # if "tags" in request_args:
    #     tag_ids = _get_tags(request_args["tags"])
    #     extra_args["fields"]["tags"] = {
    #         "value": tag_ids,
    #         "op": "in"
    #     }

    data = ctrl_collection_base.get(Bookmarks)
    return jsonify(data)


# def _get_tags(tag_args: list) -> list:
#     """Get Tag.ids if we have tags to search through."""
#     tags = []
#     if "," in tag_args:
#         tags = tag_args.split(",")
#     else:
#         tags = [tag_args]
#     tag_col = Tags()
#     tag_ids = tag_col.get_tag_ids_by_user_and_name(glow.user["user_id"], tags)
#     return tag_ids

# End File: politeauthority/bookmarky/src/bookmarky/api/controllers/collections/ctrl_bookmarks.py
