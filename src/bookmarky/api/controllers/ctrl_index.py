"""
    Bookmarky Api
    Controller - Index
    {API_URL}/

"""
import logging

from flask import Blueprint, jsonify, request, Response

from bookmarky.shared.utils import date_utils
# from bookmarky.api.stats import totals
# from bookmarky.api.stats import tasks as tasks_stats
from bookmarky.api.utils import auth
from bookmarky.api.utils import glow
from bookmarky.api.version import version
from bookmarky.api.models.user import User
from bookmarky.migrations.migrate import CURRENT_MIGRATION

ctrl_index = Blueprint("index", __name__, url_prefix="/")


@ctrl_index.route("/")
def index() -> Response:
    logging.info("Serving /")
    data = {
        "info": "Bookmarky",
        "version": version,
        "env": glow.general["CVER_ENV"],
        "build": glow.general["CVER_BUILD"],
        "build_short": glow.general["CVER_BUILD_SHORT"],
    }
    return jsonify(data)


@ctrl_index.route("/auth", methods=["POST"])
def authenticate() -> Response:
    """Authentication route. Take a Client-Id and X-Api-Key header and attempt to verify those
    credentials. Then return a JWT back to the user which can be used to authenticate all other
    requests.
    """
    logging.debug("Starting authentication flow")
    data = {
        "message": "Failed login",
        "status": "Error"
    }
    if "X-Api-Key" not in request.headers or "Client-Id" not in request.headers:
        if not "X-Api-Key" not in request.headers:
            data["message"] = "No api key sent with request."
            logging.warning("No api key sent with request")
        elif "Client-Id" not in request.headers:
            data["message"] = "No client id sent with request"
            logging.warning("No client id sent with request")
        return jsonify(data), 400

    # Try to authenticate
    client_id = request.headers["Client-Id"]
    api_key_raw = request.headers["X-Api-Key"]
    authed_event = auth.verify_api_key(client_id, api_key_raw)
    if not authed_event:
        logging.warning("Failed login attempt, client_id: %s" % client_id)
        return jsonify(data), 403
    logging.info("Verified api key")

    user = User()
    user.get_by_id(authed_event["user_id"])
    glow.user["user_id"] = user.id
    glow.user["org_id"] = user.org_id
    glow.user["role_id"] = user.role_id
    auth.record_last_access(user, authed_event["api_key"])

    # Mint the JWT
    data["token"] = auth.mint_jwt()
    data["message"] = "Authenticated user and minted token"
    data["status"] = "Success"
    logging.info("Sending back the token to the client")
    return jsonify(data)


@ctrl_index.route("/info")
@auth.auth_request
def info() -> Response:
    """Get information on model totals and task success reports."""
    # model_totals = totals.get_model_totals()
    # task_totals = tasks_stats.get_task_totals()
    data = {
        "info": "Cver Api",
        "version": glow.general["VERSION"],
        "env": glow.general["CVER_ENV"],
        "build": glow.general["CVER_BUILD"],
        "build_short": glow.general["CVER_BUILD_SHORT"],
        "migration": CURRENT_MIGRATION,
        # "tasks": task_totals,
        # "model_totals": model_totals,
        "deployed_at": glow.general["CVER_DEPLOYED_AT"]
    }
    return jsonify(data)


@ctrl_index.route("/who-am-i")
@auth.auth_request
def who_am_i() -> Response:
    """Tells a user what User the Api believes them to be."""
    token_details = auth.validate_jwt(request.headers["token"])
    token_details["expiration_date"] = date_utils.json_date_out(
        date_utils.from_epoch(token_details["exp"]))
    token_details["issue_date"] = date_utils.json_date_out(
        date_utils.from_epoch(token_details["iat"]))
    user = User()
    user.get_by_id(token_details["user_id"])
    data = {
        "status": "success",
        "token": token_details,
        "user": user.json()
    }
    return jsonify(data)


@ctrl_index.route("/healthz")
def healthz() -> Response:
    data = {
        "status": "Success",
        "message": "Healthy"
    }
    if glow.general["CVER_LOG_HEALTH_CHECKS"]:
        logging.info("Helath check, reporting healthy")
    return jsonify(data)


@ctrl_index.route("/debug")
def debug() -> Response:
    data = {
        "info": "Cver Api",
        "version": glow.general["VERSION"],
        "env": glow.general["CVER_ENV"],
        "build": glow.general["CVER_BUILD"]
    }
    if glow.general["CVER_TEST"]:
        data["test"] = True
    return jsonify(data)


# End File: politeauthroity/bookmarky/src/bookmarky/api/controllers/ctrl_index.py
