"""
    Bookmarky Shared
    Model - Bookmark

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
    "tags": {
        "name": "tags",
        "type": "list",
        "api_writeable": True,
        "api_searchable": True,
    },
    "url": {
        "name": "url",
        "type": "str",
        "api_display": True,
        "api_writeable": True,
    },
    "deleted": {
        "name": "deleted",
        "type": "datetime",
        "api_searchable": True,
    }
}

FIELD_META = {
    "ux_key": ["user_id", "url"]
}


# End File: bookmarky/src/bookmarky/shared/models/bookmark.py
