"""
    Bookmark Shared
    Model - Track

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
    "bookmark_id": {
        "name": "bookmark_id",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True,
    },
}

FIELD_META = {}


# End File: politeauthority/bookmarky/src/bookmarky/shared/models/bookmark_tag.py
