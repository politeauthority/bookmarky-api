"""
    App Entry Point.
    Web application entry point.

"""
import logging
from logging.config import dictConfig

from flask import Flask, request, jsonify, Response

from modules import auth
from modules import glow
from modules.version import version


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': glow.CONFIG["general"]["log_level"],
        'handlers': ['wsgi']
    }
})


logger = logging.getLogger(__name__)
logger.propagate = True

logging.info("Running Quigley-Api v%s" % version)
app = Flask(__name__)


@app.before_request
def before_request() -> None:
    """Before we route the request log some info about the request"""
    logging.info(
        "[Start Request] path: %s | method: %s" % (
            request.path,
            request.method))
    return


@app.after_request
def after_request(response: Response) -> Response:
    """Log the details after a response."""
    logging.info(
        "[End Request] response: %s | path: %s | method: %s" % (
            response.status_code,
            request.path,
            request.method))
    return response


@app.errorhandler(404)
def page_not_found(e: str) -> Response:
    """404 Error page."""
    data = {
        "status": "Error",
        "message": "Forbidden"
    }
    return jsonify(data), 403


@app.errorhandler(400)
def bad_request(e: str) -> Response:
    """400 Error page."""
    data = {
        "status": "Error",
        "message": "Bad Request"
    }
    return jsonify(data), 400


@app.errorhandler(403)
def not_authorized(e: str) -> Response:
    """403 Not Authorized."""
    data = {
        "status": "Error",
        "message": "Not authorized"
    }
    return jsonify(data), 403


@app.route('/', methods=["GET"])
@auth.auth_request
def index() -> Response:
    """Api Index"""
    data = {"status": "Success"}
    return jsonify(data)


@app.route('/info', methods=["GET"])
@auth.auth_request
def info() -> Response:
    """Api Info"""
    data = {
        "status": "Success",
        "version": version,
        "env": glow.CONFIG["general"]["env"]
    }
    return jsonify(data)


@app.route('/startupz', methods=["GET"])
def startup() -> Response:
    """Startup check for Quigley Api.
    We're gonna try something fun here and publish a message to Matrix. This might not be a good 
    idea.
    @todo: This has to be authenticated or made only by a local IP.
    """
    data = {"status": "Success"}
    return jsonify(data)


@app.route('/healthz', methods=["GET"])
def healthz() -> str:
    """Helath check"""
    data = {"status": "Success"}
    return jsonify(data)


if __name__ == '__main__':
    port = 80
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host="0.0.0.0", port=port, debug=True)


# End File: politeauthority/bookmarky/src/bookmarky/web-app.py
