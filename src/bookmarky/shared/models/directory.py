"""
    Bookmarky Shared
    Model - Directory

"""

FIELD_MAP = {
    "id": {
        "name": "id",
        "type": "int",
        "primary": True,
        "api_searchable": True,
    },
    "created_ts": {
        "name": "created_ts",
        "type": "datetime",
        "api_searchable": True,
    },
    "updated_ts": {
        "name": "updated_ts",
        "type": "datetime",
        "api_searchable": True,
    },
    "user_id": {
        "name": "user_id",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True,
    },
    "parent_id": {
        "name": "parent_id",
        "type": "str",
        "api_display": True,
        "api_writeable": True,
    },
    "name": {
        "name": "name",
        "type": "str",
        "api_display": True,
        "api_writeable": True,
    },
    "slug": {
        "name": "slug",
        "type": "str",
        "api_display": True,
        "api_writeable": True,
    },
    "deleted": {
        "name": "deleted",
        "type": "bool",
        "api_searchable": True,
        "api_display": False,
    },
    "hidden": {
        "name": "hidden",
        "type": "datetime",
        "api_searchable": True,
        "api_display": True,
    }
}

FIELD_META = {
    "ux_key": ["user_id", "name", "parent_id"]
}


# End File: politeauthority/bookmarky-api/src/bookmarky/shared/models/directory.py
