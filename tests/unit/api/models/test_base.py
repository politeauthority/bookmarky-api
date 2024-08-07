"""
    Bookmarky Api - Test Unit
    Api Model - Base
    Tests File: bookmarks-api/src/bookmarky/api/models/base.py
    @todo: Many of these tests could stand to be expanded out to test more types and complex models.

"""
from datetime import datetime
from dateutil.tz import tzutc
import json

import arrow
from pytest import raises

from bookmarky.api.models.base import Base

from bookmarky_test_tools.fixtures import db


BASE_MAP = {
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
    }
}
TEST_MAP = {
    "name": {
        "name": "name",
        "type": "str"
    },
    "test_int": {
        "name": "test_int",
        "type": "int",
    },
    "test_list": {
        "name": "test_list",
        "type": "list",
    },
    "test_str": {
        "name": "test_str",
        "type": "str",
    },
    "test_date": {
        "name": "test_date",
        "type": "datetime",
    },
    "test_bool": {
        "name": "test_bool",
        "type": "bool",
    },
}


class TestApiModelBase:

    def test____init__(self):
        """Test the Base Model's initialization.
        :method: Base().__init__
        """
        base = Base()
        assert hasattr(base, "iodku")
        assert hasattr(base, "immutable")
        assert hasattr(base, "insert_iodku")

        assert hasattr(base, "table_name")
        assert hasattr(base, "entity_name")
        assert hasattr(base, "field_map")
        assert hasattr(base, "field_meta")
        assert hasattr(base, "id")
        assert hasattr(base, "backed_iodku")
        assert hasattr(base, "backend")
        assert hasattr(base, "skip_fields")
        assert hasattr(base, "ux_key")
        assert hasattr(base, "conn")
        assert hasattr(base, "cursor")

    def test____repr__(self):
        """Test the Base Model's representation.
        :method: Base().__repr__
        """
        base = Base()
        assert str(base) == "<Base>"
        base.id = 5
        assert str(base) == "<Base: 5>"

    def test____desc__(self):
        """Tests that a model builds out it's field description
        :method: Base().__desc__
        """
        base = Base()
        base.field_map = BASE_MAP
        base.setup()
        base.id = 7
        assert base.__desc__() is None

    def test__connect(self):
        """
        :method: Base().connect
        """
        base = Base()
        base.total_map = BASE_MAP
        assert base.connect("conn", "cursor")
        assert hasattr(base, "conn")
        assert base.conn == "conn"
        assert hasattr(base, "cursor")
        assert base.cursor == "cursor"

    def test__setup(self):
        """Test the setup method
        @todo: Make sure we actually test something here.
        :method: Base().setup()
        """
        base = Base()
        assert base.setup()

    # def test__save(self):
    #     """
    #     :method: Base().save()
    #     @todo: Fix this @psql
    #     """
    #     base = Base(db.Conn(), db.Cursor())
    #     base.table_name = "base_table"
    #     FIELD_MAP = BASE_MAP
    #     FIELD_MAP["new_field"] = {
    #         "name": "new_field",
    #         "type": "str"
    #     }
    #     base.field_map = FIELD_MAP
    #     base.setup()
    #     BASE_MAP.pop("new_field")
    #     assert base
    #     assert not base.id, None
    #     assert base.save()
    #     assert isinstance(base.id, int)

    def test__insert(self):
        """Test that we can create a proper insert statement and set the id of a field correctly.
        :method: Base().insert()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [
            10,
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            6,
            ["hello", "world"],
            "whatsup",
            datetime(2024, 1, 1, 0, 0, tzinfo=tzutc()),
            True
        ]

        test_map = BASE_MAP
        test_map.update(TEST_MAP)
        base = Base(db.Conn(), cursor)
        base.field_map = BASE_MAP
        base.setup()
        base.test_int = 6
        base.test_list = ["hello", "world"]
        base.test_str = "whatsup"
        base.test_date = arrow.get("2024-01-1")
        base.test_bool = True
        assert not base.id
        assert base.insert()
        assert base.id == 10

    # def test__update(self):
    #     """
    #     @todo: Fix this @psql
    #     """
    #     return

    def test__delete(self):
        """Test that we can delete an entity given the model has an ID
        :@todo: Make sure that we fail as expected when we dont have an ID.
        :method: Base().delete()
        """
        base = Base(db.Conn(), db.Cursor())
        base.table_name = "base"
        base.setup()
        base.id = 5
        assert base
        assert base.delete()

    def test__get_by_id(self):
        """
        :@atodo: Test failure scenarios, such as not having an ID field and more.
        :method: Base().get_by_id()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [
            10,
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            "test_model",
            6,
            ["hello", "world"],
            "whatsup",
            datetime(2024, 1, 1, 0, 0, tzinfo=tzutc()),
            True
        ]
        test_map = BASE_MAP
        test_map.update(TEST_MAP)
        base = Base(db.Conn(), cursor)
        base.field_map = BASE_MAP
        base.setup()
        base.name = "test_model"
        base.test_int = 6
        base.test_list = ["hello", "world"]
        base.test_str = "whatsup"
        base.test_date = arrow.get("2024-01-1")
        base.test_bool = True
        assert base.get_by_id(10)

    def test__get_by_name(self):
        """
        :method: Base().get_by_name()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [
            10,
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            "test_model",
            6,
            ["hello", "world"],
            "whatsup",
            datetime(2024, 1, 1, 0, 0, tzinfo=tzutc()),
            True
        ]
        test_map = BASE_MAP
        test_map.update(TEST_MAP)
        base = Base(db.Conn(), cursor)
        base.field_map = BASE_MAP
        base.setup()
        base.name = "test_model"
        base.test_int = 6
        base.test_list = ["hello", "world"]
        base.test_str = "whatsup"
        base.test_date = arrow.get("2024-01-1")
        base.test_bool = True
        assert base.get_by_name("test_name")

    def test__get_by_field(self):
        """
        :method: Base().get_by_field()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [
            10,
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            "test_model",
            6,
            ["hello", "world"],
            "whatsup",
            datetime(2024, 1, 1, 0, 0, tzinfo=tzutc()),
            True
        ]
        test_map = BASE_MAP
        test_map.update(TEST_MAP)
        base = Base(db.Conn(), cursor)
        base.field_map = BASE_MAP
        base.setup()
        base.name = "test_model"
        base.test_int = 6
        base.test_list = ["hello", "world"]
        base.test_str = "whatsup"
        base.test_date = arrow.get("2024-01-1")
        base.test_bool = True
        assert base.get_by_field(field_name="test_int", field_value=10)

    def test__get_by_fields(self):
        """
        :method: Base().get_by_fields()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [
            10,
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            "test_model",
            6,
            ["hello", "world"],
            "whatsup",
            datetime(2024, 1, 1, 0, 0, tzinfo=tzutc()),
            True
        ]
        test_map = BASE_MAP
        test_map.update(TEST_MAP)
        base = Base(db.Conn(), cursor)
        base.field_map = test_map
        base.setup()
        base.name = "test_model"
        base.test_int = 6
        base.test_list = ["hello", "world"]
        base.test_str = "whatsup"
        base.test_date = arrow.get("2024-01-1")
        base.test_bool = True
        query = [
            {
                "field": "test_int",
                "value": 10,
                "op": "="
            },
            {
                "field": "name",
                "value": "test_model",
                "op": "eq"
            }
        ]
        assert base.get_by_fields(query)

    def test__get_by_ux_key(self):
        """
        :@todo: Test scenarios where user input can be wrong.
        :method: Base().get_by_ux_key()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [
            10,
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            "test_model",
            6,
            ["hello", "world"],
            "whatsup",
            datetime(2024, 1, 1, 0, 0, tzinfo=tzutc()),
            True
        ]
        test_map = BASE_MAP
        test_map.update(TEST_MAP)
        base = Base(db.Conn(), cursor)
        base.field_map = test_map
        base.ux_key = ["name", "test_int"]
        base.setup()
        base.name = "test_model"
        base.test_int = 6
        base.test_list = ["hello", "world"]
        base.test_str = "whatsup"
        base.test_date = arrow.get("2024-01-1")
        base.test_bool = True
        assert base.get_by_ux_key(name="test_model", test_int=6)

    def test__get_last(self):
        """
        :method: Base().get_last()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [
            10,
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            "test_model",
            6,
            ["hello", "world"],
            "whatsup",
            datetime(2024, 1, 1, 0, 0, tzinfo=tzutc()),
            True
        ]
        test_map = BASE_MAP
        test_map.update(TEST_MAP)
        base = Base(db.Conn(), cursor)
        base.field_map = test_map
        base.setup()
        base.name = "test_model"
        base.test_int = 5
        base.test_list = ["hello", "world"]
        base.test_str = "whatsup"
        base.test_date = arrow.get("2024-01-1")
        base.test_bool = True
        # import ipdb; ipdb.set_trace()
        assert not base.id
        assert base.get_last()
        assert base.id == 10

    def test__get_field(self):
        """Test that we can get a model attribute from an entity.
        :method: Base().get_field()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [
            10,
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            "test_model",
            6,
            ["hello", "world"],
            "whatsup",
            datetime(2024, 1, 1, 0, 0, tzinfo=tzutc()),
            True
        ]
        test_map = BASE_MAP
        test_map.update(TEST_MAP)
        base = Base(db.Conn(), cursor)
        base.field_map = test_map
        base.setup()
        base.name = "test_model"
        base.test_int = 6
        base.test_list = ["hello", "world"]
        base.test_str = "whatsup"
        base.test_date = arrow.get("2024-01-1")
        base.test_bool = True
        expected_name = {
            "name": "name",
            "type": "str"
        }
        assert expected_name == base.get_field("name")

    def test__build_from_list(self):
        """Test that we can hydrate a model from a list, in the way that we would recieve it back
        from Postgres.
        @todo: test raised exceptions
        :method: Base().build_from_list()
        """
        test_record = [
            10,
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            "test_model",
            6,
            ["hello", "world"],
            "whatsup",
            datetime(2024, 1, 1, 0, 0, tzinfo=tzutc()),
            True
        ]
        cursor = db.Cursor()
        cursor.result_to_return = test_record
        test_map = BASE_MAP
        test_map.update(TEST_MAP)
        base = Base(db.Conn(), cursor)
        base.field_map = test_map
        base.setup()
        assert base.build_from_list(test_record)
        assert 10 == base.id
        assert isinstance(base.created_ts, datetime)
        assert isinstance(base.updated_ts, datetime)
        # with raises(AttributeError):
        #     test_record_error = test_record
        #     test_record_error.append("hello-world")
        #     base.build_from_list(test_record_error)

    def test__build_from_dict(self):
        """
        :@todo: This can be expanded to handle more types.
        :method: Base().build_from_dict()
        """
        base = Base()
        base.field_map = BASE_MAP
        base.setup()
        test_record = {
            "id": 5,
            "created_ts": datetime.now(),
            "updated_ts": datetime.now()
        }
        assert base.build_from_dict(test_record)
        assert 5 == base.id
        assert isinstance(base.created_ts, datetime)
        assert isinstance(base.updated_ts, datetime)

    def test__check_required_class_vars(self):
        """
        :method: Base().check_required_class_vars
        """
        base = Base()
        with raises(AttributeError):
            base.check_required_class_vars()

        base = Base(db.Conn(), db.Cursor())
        assert base.check_required_class_vars()

    def test__get_dict(self):
        """Test that we return all field values from a model back as a dictionary.
        :method: Base().get_dict()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [
            10,
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            "test_model",
            6,
            ["hello", "world"],
            "whatsup",
            datetime(2024, 1, 1, 0, 0, tzinfo=tzutc()),
            True
        ]
        test_map = BASE_MAP
        test_map.update(TEST_MAP)
        base = Base(db.Conn(), cursor)
        base.field_map = test_map
        base.setup()
        base.name = "test_model"
        base.test_int = 6
        base.test_list = ["hello", "world"]
        base.test_str = "whatsup"
        base.test_date = arrow.get("2024-01-1")
        base.test_bool = True
        expected = {
            "id": None,
            "created_ts": None,
            "updated_ts": None,
            "name": "test_model",
            "test_int": 6,
            "test_list": ['hello', 'world'],
            "test_str": "whatsup",
            "test_date": arrow.get(2024, 1, 1),
            'test_bool': True
        }
        assert expected == base.get_dict()

    def test__apply_dict(self):
        """Test that we can apply a dictionary of values mapped to the model, and hydrate an entity
        with it.
        @todo: Flush this out with more assertions
        :method: Base().apply_dict()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [
            10,
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            "test_model",
            6,
            ["hello", "world"],
            "whatsup",
            datetime(2024, 1, 1, 0, 0, tzinfo=tzutc()),
            True
        ]
        test_map = BASE_MAP
        test_map.update(TEST_MAP)
        base = Base(db.Conn(), cursor)
        base.field_map = test_map
        base.setup()
        the_dict = {
            "name":  "test_model",
            "test_int": 6,
            "test_list": ["hello", "world"],
            "test_str": "whatsup",
            "test_date": arrow.get("2024-01-1"),
            "test_bool": True
        }
        assert base.apply_dict(the_dict)
        assert base.name == "test_model"

    def test__json(self):
        """Test that we can create a return which is a Jsonable dict of data, despite it being a
        dictionary output.
        :method: Base().json()
        :@todo: Make sure that types, especially dates can be converted back.
        :@todo: Expand testing for get_api
        """
        cursor = db.Cursor()
        cursor.result_to_return = [
            10,
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            datetime(2024, 4, 10, 17, 21, 26, 206683, tzinfo=tzutc()),
            "test_model",
            6,
            ["hello", "world"],
            "whatsup",
            datetime(2024, 1, 1, 0, 0, tzinfo=tzutc()),
            True
        ]
        test_map = BASE_MAP
        test_map.update(TEST_MAP)
        base = Base(db.Conn(), cursor)
        base.field_map = test_map
        base.setup()
        base.name = "test_model"
        base.test_int = 6
        base.test_list = ["hello", "world"]
        base.test_str = "whatsup"
        base.test_date = arrow.get("2024-01-1")
        base.test_bool = True
        the_json = base.json()
        assert json.dumps(the_json)
        assert isinstance(the_json, dict)
        assert isinstance(the_json["test_list"], list)
        assert isinstance(the_json["test_date"], str)
        assert isinstance(the_json["test_bool"], bool)

    def test__create_table_sql(self):
        """
        :method: Base().create_table_sql()
        """
        test_map = BASE_MAP
        test_map.update(TEST_MAP)
        base = Base()
        base.field_map = test_map
        base.setup()
        expected = ""
        result = base.create_table_sql()
        expected = "CREATE TABLE IF NOT EXISTS None\nSERIAL PRIMARY KEY,\n\n"
        expected += "TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,"
        expected += "\n\nTIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,\n"
        expected += "name VARCHAR,\ntest_int INTEGER,\ntest_list TEXT[],\n"
        expected += "test_str VARCHAR,\ntest_date TIMESTAMP,\ntest_bool BOOLEAN"
        assert expected == result

    # def test___gen_insert_sql(self):
    #     """Check that we create a correct SQL statement for an insert.
    #     :method: Base()._gen_insert_sql
    #     :@todo: not working @psql issue maybe
    #     """
    #     base = Base(None, None)
    #     base.table_name = "base"
    #     base.field_map = BASE_MAP
    #     base.setup()
    #     result = base._gen_insert_sql()
    #     assert len(result) == 127
    #     expected = 'INSERT INTO `base` (`created_ts`, `updated_ts`) VALUES ('
    #     assert result[:56] == expected

    # def test____gen_iodku_sql(self):
    #     """Check that we create a correct SQL statement for an insert.
    #     :method: Base()._gen_iodku_sql
    #     :@todo: not working @psql issue maybe
    #     """
    #     base = Base(None, None)
    #     base.table_name = "base"
    #     base.field_map = BASE_MAP
    #     base.setup()
    #     base.id = 5
    #     result = base._gen_iodku_sql()
    #     assert 314 == len(result)

    def test__gen_insert_statement(self):
        """Check that we create a correct SQL statement for a insert.
        :method: Base()._gen_insert_statement
        """
        insert_map = BASE_MAP
        insert_map.update(TEST_MAP)

        base = Base()
        base.table_name = "base"
        base.field_map = insert_map
        base.setup()
        base.name = "test_model"
        base.test_int = 5
        base.test_list = ["hello", "world"]
        base.test_str = "whatsup"
        base.test_date = arrow.get("2024-01-1")
        base.test_bool = True
        expected_sql = """
            INSERT INTO base
            (name, test_int, test_list, test_str, test_date, test_bool)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        expected_values = (
            "test_model",
            5,
            ['hello', 'world'],
            'whatsup',
            datetime(2024, 1, 1, 0, 0, tzinfo=tzutc()),
            True
        )
        result = base._gen_insert_statement()
        assert expected_sql == result["sql"]
        assert expected_values == result["values"]

    def test____gen_delete_sql(self):
        """Check that we create a correct SQL statement for a delete.
        :method: Base()._gen_delete_sql_statement
        """
        base = Base()
        base.table_name = "base"
        base.field_map = BASE_MAP
        base.field_map["test_date"]
        base.setup()
        base.id = 5
        result = base._gen_delete_sql_statement()
        expected = f"""
            DELETE FROM base
            WHERE
            id = %s;
        """
        assert expected == result

    def test___gen_get_by_fields_sql(self):
        """
        :method: Base()._gen_get_by_fields_sql
        """
        SCAN_MAP = {
            "image_id": {
                "name": "image_id",
                "type": "int",
                "api_searchable": True
            },
            "image_build_id": {
                "name": "image_build_id",
                "type": "int",
                "api_searchable": True
            }
        }
        new_map = BASE_MAP
        new_map.update(SCAN_MAP)
        fields = [
            {
                "field": "image_id",
                "value": 1,
                "op": "eq"
            },
            {
                "field": "image_build_id",
                "value": 1,
                "op": "eq"
            }
        ]
        base = Base()
        base.table_name = "base"
        base.field_map = new_map
        base.setup()
        result = base._gen_get_by_fields_sql(fields)
        expected_sql = "image_id = %s AND image_build_id = %s "
        assert expected_sql == result["sql"]

        expected_values = (1, 1)
        assert expected_values == result["values"]
        BASE_MAP.pop("image_id")
        BASE_MAP.pop("image_build_id")

    # def test___gen_get_last_sql(self):
    #     """
    #     :method: Base()._gen_get_last_sql
    #     """
    #     base = Base()
    #     base.total_map = BASE_MAP
    #     base.table_name = "base"
    #     result = base._gen_get_last_sql()
    #     expected = """
    #         SELECT id,created_ts,updated_ts,name,test_int,test_list,test_str,test_date,test_bool
    #         FROM base
    #         ORDER BY created_ts DESC
    #         LIMIT 1;
    #     """
    #     assert expected == result

    def test___sql_field_value(self):
        """
        :method: Base()._sql_field_value
        """
        base = Base()
        base.table_name = "base"
        base.field_map = BASE_MAP
        field_map_info = {
            "name": "image_id",
            "type": "int"
        }
        field_data = {
            "field": "image_build_id",
            "value": None,
            "op": "eq"
        }
        assert "NULL" == base._sql_field_value(field_map_info, field_data)
        field_data = {
            "field": "image_build_id",
            "value": 1,
            "op": "eq"
        }
        assert 1 == base._sql_field_value(field_map_info, field_data)

        field_map_info = {
            "name": "name",
            "type": "str",
        }
        field_data = {
            "field": "name",
            "value": "hello",
            "op": "eq"
        }
        assert 'hello' == base._sql_field_value(field_map_info, field_data)

    def test___sql_fields(self):
        """
        :method: Base()._sql_fields()
        """
        test_map = BASE_MAP
        test_map.update(TEST_MAP)
        base = Base()
        base.field_map = TEST_MAP
        base.setup()
        expected = "name, test_int, test_list, test_str, test_date, test_bool"
        assert expected == base._sql_fields()

    def test___sql_values(self):
        """
        :method: Base()._sql_values()
        """
        test_map = BASE_MAP
        test_map.update(TEST_MAP)
        base = Base()
        base.field_map = TEST_MAP
        base.setup()
        base.name = "test_model"
        base.test_int = 5
        base.test_list = ["hello", "world"]
        base.test_str = "whatsup"
        base.test_date = arrow.get("2024-01-1")
        base.test_bool = True
        expected_params = "%s, %s, %s, %s, %s, %s"
        expected_values = (
            "test_model",
            5,
            ['hello', 'world'],
            'whatsup',
            datetime(2024, 1, 1, 0, 0, tzinfo=tzutc()),
            True
        )
        result = base._sql_values()
        assert expected_params == result["params"]
        assert expected_values == result["values"]

    # def test___gen_get_by_unique_key_sql(self):
    #     """
    #     :method: Base()._gen_get_by_unique_key_sql()
    #     :@todo: not working @psql issue maybe
    #     """
    #     new_map = BASE_MAP
    #     EXTRAS = {
    #         "image_id": {
    #             "name": "image_id",
    #             "type": "int",
    #             "api_writeable": True,
    #             "api_searchable": True,
    #         },
    #         "image_build_id": {
    #             "name": "image_build_id",
    #             "type": "int",
    #             "api_writeable": True,
    #             "api_searchable": True,
    #         },
    #         "tag": {
    #             "name": "tag",
    #             "type": "str",
    #             "api_writeable": True,
    #             "api_searchable": True,
    #         }
    #     }
    #     new_map.update(EXTRAS)
    #     base = Base()
    #     base.table_name = "base"
    #     base.field_map = new_map
    #     base.field_meta = {
    #         "unique_key": ["image_id", "image_build_id"]
    #     }
    #     fields = {
    #         "image_id": 5,
    #         "image_build_id": 10,
    #         "tag": "latest"
    #     }

    #     with raises(AttributeError):
    #         base._gen_get_by_unique_key_sql(fields)
    #     base.field_meta = {
    #         "unique_key": ["image_id", "image_build_id", "tag"]
    #     }
    #     expected = """
    #         SELECT *
    #         FROM base
    #         WHERE
    #             `image_id` = 5 AND `image_build_id` = 10 AND `tag` = "latest"
    #         LIMIT 1;
    #     """

    #     result = base._gen_get_by_unique_key_sql(fields)
    #     assert expected == result
    #     BASE_MAP.pop("image_id")
    #     BASE_MAP.pop("image_build_id")
    #     BASE_MAP.pop("tag")

    def test___gen_delete_sql_statement(self):
        """
        :unit: Base()._gen_delete_sql_statement()
        """
        base = Base(None, None)
        base.table_name = "base"
        expected = """
            DELETE FROM base
            WHERE
            id = %s;
        """
        result = base._gen_delete_sql_statement()
        assert result == expected

    def test___set_defaults(self):
        """Checks that default field types are applied to the model.
        @todo: Currently only tests bools, need to test more types.
        :method: Base()._set_defaults
        """
        FIELD_MAP = BASE_MAP
        FIELD_MAP["new"] = {
            "name": "new",
            "type": "bool",
            "default": True
        }
        FIELD_MAP["long_number"] = {
            "name": "long_number",
            "type": "int",
            "default": 0
        }
        FIELD_MAP["list_field"] = {
            "name": "list_field",
            "type": "list",
        }
        base = Base()
        base.field_map = FIELD_MAP
        set_detaults = base._set_defaults()
        assert set_detaults
        assert base.new
        assert 0 == base.long_number
        base.long_number = 25426
        set_detaults = base._set_defaults()
        assert set_detaults
        assert 25426 == base.long_number
        assert isinstance(base.list_field, list)
        assert [] == base.list_field

    def test___set_types(self):
        """
        :method: Base()._set_types()
        """
        FIELD_MAP = BASE_MAP
        FIELD_MAP["new"] = {
            "name": "new",
            "type": "bool",
            "default": True
        }
        base = Base()
        base.field_map = FIELD_MAP
        set_detaults = base._set_defaults()
        base._set_types()
        assert set_detaults
        assert base.new

    def test___xlate_field_type(self):
        """
        :method: Base()._xlate_field_type
        """
        base = Base()
        "INTEGER" == base._xlate_field_type("int")
        "DATETIME" == base._xlate_field_type("datetime")
        "DATETIME" == base._xlate_field_type("datetime")
        "VARCHAR(200)" == base._xlate_field_type("str")
        "TEXT" == base._xlate_field_type("text")
        "TINYINT(1)" == base._xlate_field_type("bool")
        "DECIMAL(10, 5)" == base._xlate_field_type("float")
        "TEXT" == base._xlate_field_type("list")
        "JSON" == base._xlate_field_type("json")

    def test___establish_db(self):
        """
        :method: Base()._establish_db()
        """
        base = Base()
        assert base._establish_db(db.Conn(), db.Cursor())

    def test___is_model_json(self):
        """
        :method: Base()._is_model_json
        """
        base = Base()
        assert not base._is_model_json()
        base.field_map = {
            "json_field": {
                "name": json,
                "type": "json"
            }
        }
        assert base._is_model_json()

    def test____get_datetime(self):
        """
        :method: Base()._get_date_time
        """
        base = Base()
        longtime = "2023-10-11 14:21:14 +00:00"
        assert isinstance(base._get_datetime(longtime), datetime)
        short_time = "2023-10-11 14:21:14"
        assert isinstance(base._get_datetime(short_time), datetime)
        assert not base._get_datetime("nothing")


# End File: politeauthority/bookmarky-api/tests/unit/api/models/test_base.py
