#!/usr/bin/env python
"""
    Cver Api
    Glow
    Global variables for the Cver Api.

"""
import os
import uuid

# from cver.api.version import version

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
    "LOG_LEVEL": os.environ.get("CVER_LOG_LEVEL", "INFO"),
    "VERSION": "dev",
    "CVER_BUILD": os.environ.get("CVER_BUILD"),
    "CVER_BUILD_SHORT": "",
    "ENV": os.environ.get("BOOKMARKY_ENV"),
    "JWT_EXPIRE_MINUTES": os.environ.get("JWT_EXPIRE_MINUTES", 60),
    "SECRET_KEY": os.environ.get("SECRET_KEY", "hello-world123"),
    "CVER_TEST": os.environ.get("CVER_TEST", False),
    "CVER_LOG_HEALTH_CHECKS": os.environ.get("CVER_LOG_HEALTH_CHECKS", False),
    "CVER_DEPLOYED_AT": os.environ.get("CVER_DEPLOYED_AT", None)
}
if general["CVER_BUILD"]:
    general["CVER_BUILD_SHORT"] = general["CVER_BUILD"][:12]
if general["CVER_TEST"] == "true":
    general["CVER_TEST"] = True
else:
    general["CVER_TEST"] = False
if general["CVER_LOG_HEALTH_CHECKS"] == "true":
    general["CVER_LOG_HEALTH_CHECKS"] = True
else:
    general["CVER_LOG_HEALTH_CHECKS"] = False

# Store Current User Info
global user
user = {
    "user_id": None,
    "org_id": None,
    "role_id": None,
    "role_perms": None,
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


# End File: cver/src/cver/api/utils/glow.py
