"""

"""
import os

LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG")

log_config = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s %(module)s: %(message)s",
            "datefmt": "%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "default"
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["wsgi"]
    },
    "requests": {
        "level": "warning"
    }
}

# End File: bookmarky/src/bookmarky/shared/utils/log_config.py
