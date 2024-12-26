"""
    Bookmarky Shared
    Model - Tag

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
    "name": {
        "name": "name",
        "type": "str",
        "api_writeable": True,
        "api_searchable": True,
    },
    "slug": {
        "name": "slug",
        "type": "str",
        "api_searchable": True,
        "api_display": True,
        "api_writeable": True,
    },
    "deleted": {
        "name": "deleted",
        "type": "bool",
        "api_searchable": True,
    },
    "hidden": {
        "name": "hidden",
        "type": "bool",
        "api_searchable": True,
        "api_display": True,
        "api_writeable": True,
    }
}

FIELD_META = {
    "ux_key": ["user_id", "slug"]
}


# End File: politeauthority/bookmarky/src/bookmarky/shared/models/tag.py
