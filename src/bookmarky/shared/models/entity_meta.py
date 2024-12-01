"""
    Bookmarky Api
    Shared
    Model
    EntityMeta
"""


FIELD_MAP = {
    "id": {
        "name": "id",
        "type": "int",
        "primary": True,
    },
    "created_ts": {
        "name": "created_ts",
        "type": "datetime",
    },
    "updated_ts": {
        "name": "updated_ts",
        "type": "datetime",
    },
    "entity_type": {
        "name": "entity_type",
        "type": "str",
    },
    "entity_id": {
        "name": "entity_id",
        "type": "int",
    },
    "name": {
        "name": "name",
        "type": "str",
    },
    "type": {
        "name": "type",
        "type": "str"
    },
    "value": {
        "name": "value",
        "type": "str"
    },
    "user_id": {
        "name": "user_id",
        "type": "int"
    },
}
FIELD_META = {
    "ux_key": ["entity_id", "entity_type", "name", "user_id"]
}

# End File: politeauthority/bookmarky-api/src/shared/models/entity_meta.py
