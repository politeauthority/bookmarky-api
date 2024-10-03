"""
    Bookmarky Shared
    Model - Tag Feature

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
    "tag_id": {
        "name": "tag_id",
        "type": "int",
        "api_writeable": True,
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
    "value": {
        "name": "value",
        "type": "str",
        "api_display": True,
        "api_writeable": True,
    },
    "data": {
        "name": "data",
        "type": "str",
        "api_searchable": True,
    },
}


# End File: politeauthority/bookmarky/src/bookmarky/shared/models/tag.py
