"""
    Bookmarky Api
    Controller - Inter Ops
    /inter-ops

"""
import logging
import io
import json

from flask import Blueprint, jsonify, Response, send_file

from bookmarky.api.utils import glow
from bookmarky.api.utils.export import Export
from bookmarky.api.utils import auth


ctrl_interops = Blueprint("interops", __name__, url_prefix="/inter-ops")


@ctrl_interops.route("/export")
@auth.auth_request
def export() -> Response:
    logging.info("Serving /export")
    export_data = Export().run(glow.user["user_id"])
    try:
        export_file = json.dumps(export_data)
    except Exception as e:
        logging.error("Failed to convert export to JSON: %s" % e)
        return jsonify({"stauts": "error"}), 500
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


# End File: politeauthroity/bookmarky/src/bookmarky/api/controllers/ctrl_interops.py
