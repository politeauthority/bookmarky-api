"""
    Bookmark Tag Shared
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
    "bookmark_id": {
        "name": "bookmark_id",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True,
    },
    "tag_id": {
        "name": "tag_id",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True,
    },
}

FIELD_META = {
    "ux_key": ["bookmark_id", "tag_id"]
}


# End File: politeauthority/bookmarky/src/bookmarky/shared/models/bookmark_tag.py
