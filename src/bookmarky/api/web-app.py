#!/usr/bin/env python
"""
    Bookmarky Api
    App
    Primary web app entrpoint

"""
import logging
import traceback
import sys

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

from bookmarky.shared.utils.log_config import log_config
from bookmarky.api.utils import db
from bookmarky.api.utils import glow
# from cver.api.utils import glow
# from cver.api.utils import misc
from bookmarky.api.controllers.models.ctrl_api_key import ctrl_api_key


from bookmarky.api.controllers.models.ctrl_bookmark import ctrl_bookmark
from bookmarky.api.controllers.collections.ctrl_bookmarks import ctrl_bookmarks
from bookmarky.api.controllers.collections.ctrl_api_keys import ctrl_api_keys
from bookmarky.api.controllers.ctrl_index import ctrl_index
# from cver.api.controllers.ctrl_collections.ctrl_migrations import ctrl_migrations
# from cver.api.controllers.ctrl_models.ctrl_role import ctrl_role
# from cver.api.controllers.ctrl_collections.ctrl_roles import ctrl_roles
# from cver.api.controllers.ctrl_models.ctrl_role_perm import ctrl_role_perm
# from cver.api.controllers.ctrl_collections.ctrl_role_perms import ctrl_role_perms
# from cver.api.controllers.ctrl_models.ctrl_perm import ctrl_perm
# from cver.api.controllers.ctrl_collections.ctrl_perms import ctrl_perms
from bookmarky.api.controllers.models.ctrl_user import ctrl_user
# from cver.api.controllers.ctrl_collections.ctrl_users import ctrl_users
from bookmarky.api.controllers.models.ctrl_option import ctrl_option
from bookmarky.api.controllers.collections.ctrl_options import ctrl_options


logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)
logger.propagate = True

app = Flask(__name__)
app.config.update(DEBUG=True)
app.debugger = False


def register_blueprints(app: Flask) -> bool:
    """Register controller blueprints to flask."""
    app.register_blueprint(ctrl_index)
    app.register_blueprint(ctrl_api_key)
    app.register_blueprint(ctrl_api_keys)
    app.register_blueprint(ctrl_user)
    app.register_blueprint(ctrl_option)
    app.register_blueprint(ctrl_options)
    app.register_blueprint(ctrl_bookmark)
    app.register_blueprint(ctrl_bookmarks)

    return True


@app.errorhandler(Exception)
def handle_exception(e):
    """Catch 500 errors, and pass through the exception
    @todo: Remove the exception for non prod environments.
    """
    data = {
        "message": "Server error",
        "request-id": glow.session["short_id"],
        "status": "error"
    }
    RESPONSE_CODE = 500
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        data["message"] = e.description
        return jsonify(data), RESPONSE_CODE

    traceback.print_exc(file=sys.stdout)
    print(traceback)
    if glow.general["CVER_TEST"]:
        data["message"] = traceback
        return jsonify(data), 500
    else:
        return jsonify(data), RESPONSE_CODE


@app.before_request
def before_request():
    """Before we route the request log some info about the request."""
    glow.start_session()
    logging.info(
        "[Start Request] %s\tpath: %s | method: %s" % (
            glow.session["short_id"][:8],
            request.path,
            request.method))
    db.connect()
    return


@app.after_request
def after_request(response):
    logging.info(
        "[End Request] %s\tpath: %s | method: %s | status: %s | size: %s",
        glow.session["short_id"],
        request.path,
        request.method,
        response.status,
        response.content_length
    )
    db.close()
    return response


register_blueprints(app)

# Development Runner
if __name__ == "__main__":
    logging.info("Starting develop webserver")
    app.run(host='0.0.0.0', port=80)


# Production Runner
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.debug")
    logging.info("Starting production webserver")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.config['DEBUG'] = True


# End File: bookmarky/src/bookmarky/api/app.py
