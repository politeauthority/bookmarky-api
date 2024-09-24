"""
    Bookmarky Shared
    Model  User

"""

FIELD_MAP = {
    "id": {
        'name': 'id',
        'type': 'int',
        'primary': True,
    },
    "created_ts": {
        'name': 'created_ts',
        'type': 'datetime',
    },
    "updated_ts": {
        'name': 'updated_ts',
        'type': 'datetime',
    },
    "name": {
        "name": "name",
        "type": "str",
        "api_writeable": True,
        "api_searchable": True
    },
    "email": {
        "name": "email",
        "type": "str",
        "extra": "UNIQUE",
        "api_writeable": True,
        "api_searchable": True
    },
    "role_id": {
        "name": "role_id",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True
    },
    "org_id": {
        "name": "org_id",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True
    },
    "last_access": {
        "name": "last_access",
        "type": "datetime",
        "api_searchable": True
    }
}

FIELD_MAP_METAS = {
    "display_hidden": {
        "name": "display_hidden",
        "type": "bool"
    },
    "beta_features": {
        "name": "beta_features",
        "type": "bool"
    }
}

# End File: politeauthority/bookmarky-api/src/bookmarky/shared/models/user.py
