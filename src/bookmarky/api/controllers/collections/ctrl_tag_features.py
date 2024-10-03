"""
    Bookmark Api
    Controller Collection
    Tag Features

"""
from flask import Blueprint, jsonify, Response

from bookmarky.api.collects.tags import Tags
from bookmarky.api.controllers.collections import ctrl_collection_base
from bookmarky.api.utils import auth
from bookmarky.api.utils import glow

ctrl_tag_features = Blueprint("tag-features", __name__, url_prefix="/tag-features")

PER_PAGE = 50


@ctrl_tag_features.route("")
@auth.auth_request
def index() -> Response:
    """Get Tag Features."""
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


# End File: politeauthority/bookmarky-api/src/bookmarky/api/controllers/ctrl_collections/
#           ctrl_tag_features.py
