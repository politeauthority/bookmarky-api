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

# from cver.shared.utils.log_config import log_config
from bookmarky.api.utils import db
from bookmarky.api.utils import glow
# from cver.api.utils import glow
# from cver.api.utils import misc
from bookmarky.api.controllers.models.ctrl_api_key import ctrl_api_key


from bookmarky.api.controllers.models.ctrl_bookmark import ctrl_bookmark
from bookmarky.api.controllers.collections.ctrl_bookmarks import ctrl_bookmarks
from bookmarky.api.controllers.collections.ctrl_api_keys import ctrl_api_keys

# from cver.api.controllers.models.ctrl_cluster_image import ctrl_cluster_image
# from cver.api.controllers.ctrl_collections.ctrl_cluster_images import ctrl_cluster_images
# from cver.api.controllers.ctrl_models.ctrl_cluster_image_build import (
#     ctrl_cluster_image_build)
# from cver.api.controllers.ctrl_collections.ctrl_cluster_image_builds import (
#     ctrl_cluster_image_builds)
# from cver.api.controllers.ctrl_models.ctrl_cluster import ctrl_cluster
# from cver.api.controllers.ctrl_collections.ctrl_clusters import ctrl_clusters
from bookmarky.api.controllers.ctrl_index import ctrl_index
# from cver.api.controllers.ctrl_models.ctrl_image import ctrl_image
# from cver.api.controllers.ctrl_collections.ctrl_images import ctrl_images
# from cver.api.controllers.ctrl_models.ctrl_image_build import ctrl_image_build
# from cver.api.controllers.ctrl_models.ctrl_image_build_pull import ctrl_image_build_pull
# from cver.api.controllers.ctrl_collections.ctrl_image_build_pulls import ctrl_image_build_pulls
# from cver.api.controllers.ctrl_collections.ctrl_image_build_waitings import (
#     ctrl_image_build_waitings)
# from cver.api.controllers.ctrl_models.ctrl_image_build_waiting import ctrl_image_build_waiting
# from cver.api.controllers.ctrl_collections.ctrl_image_builds import ctrl_image_builds
# from cver.api.controllers.ctrl_collections.ctrl_migrations import ctrl_migrations
# from cver.api.controllers.ctrl_collections.ctrl_registries import ctrl_registries
# from cver.api.controllers.ctrl_models.ctrl_registry import ctrl_registry
# from cver.api.controllers.ctrl_models.ctrl_role import ctrl_role
# from cver.api.controllers.ctrl_collections.ctrl_roles import ctrl_roles
# from cver.api.controllers.ctrl_models.ctrl_role_perm import ctrl_role_perm
# from cver.api.controllers.ctrl_collections.ctrl_role_perms import ctrl_role_perms
# from cver.api.controllers.ctrl_models.ctrl_perm import ctrl_perm
# from cver.api.controllers.ctrl_collections.ctrl_perms import ctrl_perms
from bookmarky.api.controllers.models.ctrl_user import ctrl_user
# from cver.api.controllers.ctrl_collections.ctrl_users import ctrl_users
# from cver.api.controllers.ctrl_models.ctrl_option import ctrl_option
# from cver.api.controllers.ctrl_collections.ctrl_options import ctrl_options
# from cver.api.controllers.ctrl_models.ctrl_scan import ctrl_scan
# from cver.api.controllers.ctrl_models.ctrl_scan_raw import ctrl_scan_raw
# from cver.api.controllers.ctrl_collections.ctrl_scan_raws import ctrl_scan_raws
# from cver.api.controllers.ctrl_collections.ctrl_scans import ctrl_scans
# from cver.api.controllers.ctrl_collections.ctrl_scanners import ctrl_scanners
# from cver.api.controllers.ctrl_models.ctrl_software import ctrl_software
# from cver.api.controllers.ctrl_models.ctrl_task import ctrl_task
# from cver.api.controllers.ctrl_collections.ctrl_tasks import ctrl_tasks
# from cver.api.controllers.ctrl_collections.ctrl_softwares import ctrl_softwares
# from cver.api.controllers.ctrl_submit_scan import ctrl_submit_scan
# from cver.api.controllers.ctrl_ingest_k8s import ctrl_ingest_k8s


# logging.config.dictConfig(log_config)
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


# End File: cver/src/cver/api/app.py
