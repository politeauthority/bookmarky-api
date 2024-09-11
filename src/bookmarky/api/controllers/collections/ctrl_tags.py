"""
    Bookmark Api
    Controller Collection
    Tags

"""
import logging

from flask import Blueprint, jsonify, request, Response

from bookmarky.api.collects.tags import Tags
from bookmarky.api.controllers.collections import ctrl_collection_base
from bookmarky.api.utils import auth
from bookmarky.api.utils import glow

ctrl_tags = Blueprint("tags", __name__, url_prefix="/tags")


@ctrl_tags.route("")
@auth.auth_request
def index() -> Response:
    """Get Tags."""
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
    data = ctrl_collection_base.get(Tags, extra_args)
    return jsonify(data)


@ctrl_tags.route("/search")
@auth.auth_request
def search() -> Response:
    """Search through Tags from a wide variety of input."""
    extra_args = {
        "fields": {},
        "order_by": {},
        "limit": None
    }
    search_args = request.args

    logging.debug(f"\n\nSEARCHING\n{search_args}\n\n")
    if "query" in search_args:
        extra_args["concat_type"] = "where_or"
        extra_args["fields"]["name"] = {
            "value": f'%{search_args["query"]}%',
            "op": "ilike",
        }
    logging.debug("\n\nTags SEARCH\n")
    logging.debug(extra_args)
    logging.debug("\nEND SEARCH\n\n")
    data = ctrl_collection_base.get(Tags, extra_args)
    return jsonify(data)


# End File: politeauthority/bookmarky-api/src/bookmarky/api/controllers/ctrl_collections/
#           ctrl_tags.py
