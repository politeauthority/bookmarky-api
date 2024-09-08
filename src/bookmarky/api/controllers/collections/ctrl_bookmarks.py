"""
    Bookmark Api
    Controller Collection
    Bookmarks

"""
import logging

from flask import Blueprint, jsonify, request

from bookmarky.api.collects.bookmarks import Bookmarks
from bookmarky.api.collects.tags import Tags
from bookmarky.api.models.tag import Tag
from bookmarky.api.controllers.collections import ctrl_collection_base
from bookmarky.api.utils import auth
from bookmarky.api.utils import glow


ctrl_bookmarks = Blueprint("bookmarks", __name__, url_prefix="/bookmarks")


@ctrl_bookmarks.route("")
@auth.auth_request
def index():
    """Get Bookmarks, along with associated Tags where they exist."""
    extra_args = {
        "fields": {
            "user_id": {
                "value": glow.user["user_id"],
                "op": "=",
                "overrideable": False
            }
        },
        "order_by": {},
        "limit": None
    }
    data = ctrl_collection_base.get(Bookmarks, extra_args)
    data["objects"] = Tags().get_tags_for_bookmarks(data["objects"])
    return jsonify(data)


@ctrl_bookmarks.route("/search")
@auth.auth_request
def search():
    """Search through Bookmarks from a wide variety of input."""
    extra_args = {
        "concat_type": "",
        "fields": {},
        "order_by": {},
        "limit": None
    }
    search_args = request.args

    logging.debug(f"\n\nSEARCHING\n{search_args}\n\n")
    if "query" in search_args:
        extra_args["concat_type"] = "where_or"
        extra_args["fields"]["title"] = {
            "value": f'%{search_args["query"]}%',
            "op": "ilike",
        }
        extra_args["fields"]["url"] = {
            "value": f'%{search_args["query"]}%',
            "op": "ilike",
        }
        extra_args["fields"]["notes"] = {
            "value": f'%{search_args["query"]}%',
            "op": "ilike",
        }
        # extra_args["fields"]["title"] = {
        #     "value": glow.user["user_id"],
        #     "op": "LIKE",
        # }
    logging.debug("\n\nBOOKMARK SEARCH\n")
    logging.debug(extra_args)
    logging.debug("\nEND SEARCH\n\n")
    data = ctrl_collection_base.get(Bookmarks, extra_args)

    if data["objects"]:
        data["objects"] = Tags().get_tags_for_bookmarks(data["objects"])
    return jsonify(data)


@ctrl_bookmarks.route("/by-tag")
@auth.auth_request
def by_tag():
    """Get Bookmarks by a Tag.
    @todo: This feels lazy, this should be done better probably.
    """
    data = {
        "info": {
            "current_page": 1,
        },
        "objects": []
    }
    search_args = request.args
    tag = Tag()
    tag.get_by_slug(search_args["tag_slug"])
    # logging.debug(f"\n\nSEARCHING\n{search_args}\n\n")
    # logging.debug("\n\nBOOKMARK BY TAG\n")
    # logging.debug("\nEND BOOKMARK BY TAG\n\n")
    bookmarks_col = Bookmarks()
    bookmarks = bookmarks_col.get_by_tag_id(tag.id)
    bookmarks_json = bookmarks_col._make_json(bookmarks)
    data["objects"] = Tags().get_tags_for_bookmarks(bookmarks_json)
    data["info"]["total_objects"] = len(data["objects"])
    return jsonify(data)

# End File: politeauthority/bookmarky-api/src/bookmarky/api/controllers/collections/
#           ctrl_bookmarks.py
