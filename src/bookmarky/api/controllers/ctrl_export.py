"""
    Bookmarky Api
    Controller - Export
    /export

"""
import logging
import io
import json

from flask import Blueprint, jsonify, Response, send_file

from bookmarky.api.utils import glow
from bookmarky.api.utils.export import Export
from bookmarky.api.utils import auth


ctrl_export = Blueprint("export", __name__, url_prefix="/export")


@ctrl_export.route("")
@ctrl_export.route("/")
@auth.auth_request
def index() -> Response:
    logging.info("Serving /export")
    export_data = Export().run(glow.user["user_id"])
    export_file = json.dumps(export_data)
    json_bytes = io.BytesIO(export_file.encode('utf-8'))
    json_bytes.seek(0)
    try:
        return send_file(
            json_bytes,
            download_name="bookmarky-export.json",
            mimetype="application/json",
            as_attachment=True
        )
    except Exception as e:
        logging.error("Error creating export: %s" % e)
        return jsonify({"stauts": "error"}), 500


# End File: politeauthroity/bookmarky/src/bookmarky/api/controllers/ctrl_export.py
