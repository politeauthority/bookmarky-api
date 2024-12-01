"""
    Bookmarky Shared
    Model
    Bookmark

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
    "title": {
        "name": "title",
        "type": "str",
        "api_searchable": True,
        "api_display": True,
        "api_writeable": True,
    },
    "url": {
        "name": "url",
        "type": "str",
        "api_display": True,
        "api_searchable": True,
        "api_writeable": True,
    },
    "deleted": {
        "name": "deleted",
        "type": "datetime",
        "api_searchable": False,
        "api_display": False,
    },
    "directory_id": {
        "name": "directory_id",
        "type": "int",
        "api_searchable": True,
        "api_display": True,
        "api_writeable": True,
    },
    "notes": {
        "name": "notes",
        "type": "text",
        "api_searchable": True,
        "api_display": True,
        "api_writeable": True,
    },
    "hidden": {
        "name": "hidden",
        "type": "bool",
        "default": False,
        "api_searchable": True,
        "api_display": True,
        "api_writeable": True,
    }
}

FIELD_META = {
    "ux_key": ["user_id", "url"]
}

FIELD_MAP_METAS = {
    "favorite": {
        "name": "favorite",
        "type": "bool"
    },
    "featured-image": {
        "name": "featured-image",
        "type": "str"
    },
    "click-count": {
        "name": "click-count",
        "type": "int"
    }
}


# End File: politeauthority/bookmark-apiy/src/bookmarky/shared/models/bookmark.py
