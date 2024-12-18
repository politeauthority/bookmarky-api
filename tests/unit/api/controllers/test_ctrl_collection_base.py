"""
    Bookmarky Test
    Unit
    CTRL Collection Base

"""
from bookmarky.api.collects.api_keys import ApiKeys
# from bookmarky.api.collects.cluster_images import ClusterImages
# from bookmarky.api.collects.images import Images
from bookmarky.api.controllers.collections import ctrl_collection_base

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
    "image_score": {
        "name": "image_score",
        "type": "int",
        "api_searchable": True,
    },
    "image_name": {
        "name": "image_name",
        "type": "str",
        "api_searchable": True,
    },
    "key": {
        "name": "key",
        "type": "str",
        "api_searchable": True,
        "api_display": False
    },
    "not_queryable": {
        "name": "not_queryable",
        "type": "str",
        "api_searchable": False,
        "api_display": False
    }
}


class TestCtrlCollectionBase:

    def test___parse_body(self):
        """
        :method: ctrl_collection_base._get_object_type
        """
        raw_args = {
            "fields": {
                "client_id": {
                    "value": 1,
                    "op": "="
                }
            },
            "order_by": {
                "field": "id",
                "direction": "ASC"
            }
        }
        result = ctrl_collection_base._parse_body(raw_args, FIELD_MAP)
        assert isinstance(result, dict)
        assert isinstance(result["where_and"], list)
        
        # assert "id" == result["order_by"]["field"]
        # assert "ASC" == result["order_by"]["direction"]
        assert not result["limit"]
        assert not result["page"]
        # assert result == [{'field': 'client_id', 'value': 1, 'op': '='}]

    def test___get_object_type(self):
        """
        :method: ctrl_collection_base._get_object_type
        """
        assert ctrl_collection_base._get_object_type(ApiKeys) == "api-key"
        # assert ctrl_collection_base._get_object_type(ClusterImages) == "cluster-image"
        # assert ctrl_collection_base._get_object_type(Images) == "image"

    def test___get_api_hidden_fields(self):
        """
        :method: ctrl_collection_base._get_api_hidden_fields
        """
        assert ["key", "not_queryable"] == ctrl_collection_base._get_api_hidden_fields(FIELD_MAP)

    def test___get_fields(self):
        """
        :method: ctrl_collection_base._get_fields
        """
        field_data = {
            "created_ts": {
                "op": ">",
                "value": "2023-10-13 01:00:00"
            },
            "image_name": {
                "op": "=",
                "value": "cool"
            }
        }

        result = ctrl_collection_base._get_fields(field_data, FIELD_MAP)
        assert isinstance(result, list)
        assert isinstance(result[0], dict)
        assert "created_ts" == result[0]["field"]

    def test___get_order_by(self):
        """
        :method: ctrl_collection_base._get_order_by
        """
        assert {} == ctrl_collection_base._get_order_by({})

        order_data = {
            "field": "id",
            "direction": "ASC",
        }
        assert order_data == ctrl_collection_base._get_order_by(order_data)

    def test___field_queryable(self):
        """
        :method: ctrl_collection_base._field_queryable
        """
        assert ctrl_collection_base._field_queryable("image_name", FIELD_MAP)
        assert not ctrl_collection_base._field_queryable("image_namey", FIELD_MAP)
        assert not ctrl_collection_base._field_queryable("not_queryable", FIELD_MAP)

    def test___query_direct(self):
        """
        :method: ctrl_collection_base._query_direct
        """
        result = ctrl_collection_base._query_direct(
            "image_name",
            "hello-world",
            FIELD_MAP["image_name"])
        assert isinstance(result, dict)
        assert "image_name" == result["field"]
        assert "hello-world" == result["value"]
        assert "=" == result["op"]

    def test___get_operation(self):
        """
        :method:ctrl_collection_base::_get_operation
        """
        query_data = {
            "op": "=",
            "value": "hello-world"
        }
        assert "=" == ctrl_collection_base._get_operation(query_data, FIELD_MAP["image_name"])
        query_data = {
            "op": "LIKE",
            "value": "hello-world"
        }
        assert "LIKE" == ctrl_collection_base._get_operation(query_data, FIELD_MAP["image_name"])

        query_data = {
            "op": ">",
            "value": "2023-10-18 01:00:00"
        }
        assert ">" == ctrl_collection_base._get_operation(query_data, FIELD_MAP["created_ts"])

        query_data = {
            "op": ">sdas",
            "value": "2023-10-18 01:00:00"
        }
        assert "=" == ctrl_collection_base._get_operation(query_data, FIELD_MAP["created_ts"])

        query_data = {
            "op": "lt",
            "value": "2023-10-18 01:00:00"
        }
        assert "<" == ctrl_collection_base._get_operation(query_data, FIELD_MAP["created_ts"])

        query_data = {
            "op": "gt",
            "value": "2023-10-18 01:00:00"
        }
        assert ">" == ctrl_collection_base._get_operation(query_data, FIELD_MAP["created_ts"])


# End File: politeauthority/bookmarky/tests/unit/api/collections/controllers/
#               test_ctrl_collection_base.py
