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

PER_PAGE = 50


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
    data = {
        "objects": [],
        "object_type": "tag",
        "message": "No search criteria",
        "status": "Error",
        "info": {
            "current_page": 1,
            "last_page": None,
            "per_page": PER_PAGE,
            "total_objects": 0,
        }
    }
    search_args = request.args
    if "query" not in search_args:
        logging.warning("No search criteria for search")
        return jsonify(data)
    if "page" in search_args:
        if search_args["page"] and search_args["page"].isdigit():
            current_page = int(search_args["page"])
    else:
        current_page = 1
    search_phrase = f"%{search_args['query']}%"
    query = _gen_search_query(search_phrase, current_page)
    logging.debug(f"\n\nSEARCHING\n{search_args}\n\n")
    tags_col = Tags()
    data["objects"] = tags_col.get_query(query["sql"], query["params"])
    data["objects"] = tags_col.make_json(data["objects"])
    data["info"] = tags_col.get_pagination_info(query, current_page, PER_PAGE)
    data["message"] = "Search successful"
    data["status"] = "Success"
    logging.debug("\nEND SEARCH\n\n")
    return jsonify(data)


def _gen_search_query(search_phrase: str, page: int) -> dict:
    """Generate the search query SQL."""
    if page == 1:
        offset = 0
    else:
        offset = (page * PER_PAGE) - PER_PAGE

    query = {
        "sql": None,
        "params": ()
    }
    query["sql"] = f"""
        SELECT *
        FROM tags
        WHERE
            user_id = %s AND
            (
                name ILIKE %s
            )
        ORDER BY created_ts DESC
        LIMIT 20 OFFSET {offset};
    """
    query["params"] = (glow.user["user_id"], search_phrase)
    return query



# End File: politeauthority/bookmarky-api/src/bookmarky/api/controllers/ctrl_collections/
#           ctrl_tags.py
