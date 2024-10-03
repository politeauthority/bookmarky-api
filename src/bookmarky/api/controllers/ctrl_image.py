"""
    Bookmarky Api
    Controller
    Image
    /image

"""
import logging
import os
import re

from flask import Blueprint, Response, send_from_directory, jsonify

from bookmarky.api.utils import auth
from bookmarky.api.utils import glow

IMAGE_DIR = glow.general["IMAGE_DIR"]

ctrl_image = Blueprint("image", __name__, url_prefix="/image")


@ctrl_image.route("/<image_name>")
@auth.auth_request
def image(image_name: str) -> Response:
    error = {
        "status": "error",
        "message": "Forbidden"
    }
    if not IMAGE_DIR:
        logging.error("No IMAGE_DIR set for current environment")
        return jsonify(error, 500)
    if not is_safe_filename(image_name):
        return jsonify(error), 403
    image_path = os.path.join(IMAGE_DIR, image_name)
    if not os.path.exists(image_path):
        error["message"] = "Not Found"
        return jsonify(error), 404
    logging.info("Serving /image/%s" % image_name)
    return send_from_directory(IMAGE_DIR, image_name), 200


def is_safe_filename(filename):
    # Only allow alphanumeric characters, underscores, and dots (for file extensions)
    return re.match(r'^[\w\-.]+$', filename) is not None

# End File: politeauthroity/bookmarky/src/bookmarky/api/controllers/ctrl_image.py
