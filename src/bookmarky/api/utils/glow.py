#!/usr/bin/env python
"""
    Bookmarky Api
    Utils - Glow
    Global variables for the Bookmarky Api.

"""
import os
import uuid

from bookmarky.api.version import version

global db
db = {
    "conn": "",
    "cursor": "",
    "HOST": os.environ.get("BOOKMARKY_DB_HOST"),
    "PORT": os.environ.get("BOOKMARKY_DB_PORT", 5432),
    "NAME": os.environ.get("BOOKMARKY_DB_NAME"),
    "USER": os.environ.get("BOOKMARKY_DB_USER"),
    "PASS": os.environ.get("BOOKMARKY_DB_PASS"),
}

# Load Cver Options
global options
options = {}

# Collect General Details
global general
general = {
    "LOG_LEVEL": os.environ.get("LOG_LEVEL", "INFO"),
    "VERSION": version,
    "BUILD": os.environ.get("BUILD"),
    "BUILD_SHORT": "",
    "ENV": os.environ.get("BOOKMARKY_ENV"),
    "JWT_EXPIRE_MINUTES": os.environ.get("JWT_EXPIRE_MINUTES", 60),
    "SECRET_KEY": os.environ.get("SECRET_KEY", "hello-world123"),
    "TEST": os.environ.get("TEST", False),
    "LOG_HEALTH_CHECKS": os.environ.get("LOG_HEALTH_CHECKS", True),
    "DEPLOYED_AT": os.environ.get("DEPLOYED_AT", None),
    "IMAGE_DIR": os.environ.get("PUBLIC_IMAGES", "/images"),
    # "IMAGE_DIR": "/work/src/bookmarky/public/images",
}
if general["BUILD"]:
    general["BUILD_SHORT"] = general["BUILD"][:12]
if general["TEST"] == "true":
    general["TEST"] = True
else:
    general["TEST"] = False
if general["LOG_HEALTH_CHECKS"] == "true":
    general["LOG_HEALTH_CHECKS"] = True
else:
    general["LOG_HEALTH_CHECKS"] = False

# Store Current User Info
global user
user = {
    "user_id": None,
    "org_id": None,
    "role_id": None,
    "role_perms": None,
    "obj": None,
}

global session
session = {
    "uuid": None,
    "short-id": None,
}


def start_session():
    session["uuid"] = str(uuid.uuid1())
    session["short_id"] = session["uuid"][:8]
    return True


# End File: politeauthority/bookmarky-api/src/bookmarky/api/utils/glow.py
