"""
    Bookmarky Shared
    Model - Migrate

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
    "number": {
        "name": "number",
        "type": "int",
    },
    "success": {
        "name": "success",
        "type": "bool",
    }
}

# End File: politeauthority/bookmarky-api/src/bookmarky/shared/models/migrate.py
