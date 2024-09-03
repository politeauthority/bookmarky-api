"""
    Bookmarky Api
    Controller
    Stats
    /stats

"""
import logging

from flask import Blueprint, jsonify, Response

# from bookmarky.api.stats import totals
from bookmarky.api.collects.tags import Tags
from bookmarky.api.utils import auth
from bookmarky.api.utils import glow

ctrl_stats = Blueprint("stats", __name__, url_prefix="/stats")


@auth.auth_request
@ctrl_stats.route("/top-tags")
def top_tags() -> Response:
    """Get the Tags which have the most relationships."""
    logging.info("Serving /")
    data = {
        "info": "Bookmarky",
        "objects": []
    }
    sql = """
        SELECT tag_id, COUNT(tag_id) AS tag_count
        FROM bookmark_tags
        GROUP BY tag_id
        ORDER BY tag_count DESC
        LIMIT 10;
    """
    glow.db["cursor"].execute(sql)
    rows = glow.db["cursor"].fetchall()
    print(rows)
    tag_ids = _get_ids(rows)
    tag_col = Tags()
    tags = tag_col.get_by_ids(tag_ids)
    for tag in tags:
        data["objects"].append(tag.json())
    return jsonify(data)


def _get_ids(rows) -> list:
    """Generate a list of Tag IDs from a result set."""
    ret_ids = []
    for row in rows:
        ret_ids.append(row[0])
    return ret_ids

# End File: politeauthroity/bookmark-apiy/src/bookmarky/api/controllers/ctrl_stats.py
