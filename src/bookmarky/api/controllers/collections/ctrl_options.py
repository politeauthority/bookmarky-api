"""
    Cver Api - Controller Collection
    Options

"""

from flask import Blueprint, jsonify

from bookmarky.api.collects.options import Options
from bookmarky.api.controllers.collections import ctrl_collection_base
from bookmarky.api.utils import auth

ctrl_options = Blueprint('options', __name__, url_prefix='/options')


@ctrl_options.route('')
@auth.auth_request
def index():
    data = ctrl_collection_base.get(Options)
    return jsonify(data)


# End File: bookmarky/src/bookmarky/api/controllers/ctrl_collections/ctrl_options.py
