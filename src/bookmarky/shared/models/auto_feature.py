"""
    Bookmarky Shared
    Model
    Auto Feature

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
    "entity_id": {
        "name": "entity_id",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True,
    },
    "entity_type": {
        "name": "entity_type",
        "type": "str",
        "api_display": True,
        "api_searchable": True,
        "api_writeable": True,
    },
    "auto_feature_type": {
        "name": "auto_feature_type",
        "type": "str",
        "api_display": True,
        "api_searchable": True,
        "api_writeable": True,
    },
    "auto_feature_value": {
        "name": "auto_feature_value",
        "type": "str",
        "api_display": True,
        "api_searchable": True,
        "api_writeable": True,
    },
    "enabled": {
        "name": "enabled",
        "type": "bool",
        "default": False,
        "api_searchable": True,
        "api_display": True,
        "api_writeable": True,
    }
}

FIELD_META = {
    "ux_key": ["user_id", "entity_id", "entity_type", "auto_feature_type", "auto_feature_value"]
}


# End File: politeauthority/bookmark-apiy/src/bookmarky/shared/models/auto_feature.py
