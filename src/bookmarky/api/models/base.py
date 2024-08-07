"""
    Cver Api
    Base Model v. 0.4.0
    Parent class for all models to inherit, providing methods for creating tables, inserting, updating,
    selecting and deleting data.

"""
from datetime import datetime, date
import json
import logging

import arrow
import psycopg2

from polite_lib.utils import xlate
from polite_lib.utils import date_utils

from bookmarky.api.utils import glow


class Base:

    def __init__(self, conn=None, cursor=None):
        """Base model constructor
        :unit-test: TestApiModelBase::test____init__
        """
        self._establish_db(conn, cursor)
        self.iodku = False
        self.immutable = False
        self.insert_iodku = False

        self.table_name = None
        self.entity_name = None
        self.field_map = {}
        self.field_meta = {}

        self.id = None
        self.backed_iodku = True
        self.backend = "postgres"
        self.skip_fields = ["id", "created_ts", "updated_ts"]
        self.ux_key = []
        self.setup()

    def __repr__(self):
        """Base model representation
        :unit-test: TestApiModelBase::test____repr__
        """
        if self.id:
            return "<%s: %s>" % (self.__class__.__name__, self.id)
        return "<%s>" % self.__class__.__name__

    def __desc__(self) -> None:
        """Describes the fields and values of class.
        :unit-test: TestApiModelBase::test____repr__
        """
        for field_id, field in self.field_map.items():
            print("%s: %s" % (field["name"], getattr(self, field["name"])))

    def connect(self, conn, cursor) -> bool:
        """Quick bootstrap method to connect the model to the database connection.
        :unit-test: TestApiModelBase::test__connect
        """
        self.conn = conn
        self.cursor = cursor
        return True

    def setup(self) -> bool:
        """Set up model class vars, sets class var defaults, and corrects types where possible.
        :unit-test: TestApiModelBase::test__setup
        """
        self._set_defaults()
        self._set_types()
        return True

    def save(self) -> bool:
        """Saves a model instance in the model table.
        :unit-test: TestApiModelBase::test__save
        """
        self.setup()
        self.check_required_class_vars()
        if self._is_model_json():
            return self.insert()
        if self.backed_iodku and self.insert_iodku:
            if self.id:
                return self.iodku()
            else:
                return self.insert()
        else:
            if self.id:
                return self.update()
            else:
                return self.insert()

    def insert(self) -> bool:
        """Insert a new record of the model.
        :unit-test: TestApiModelBase::test__insert
        """
        statement = self._gen_insert_statement()
        try:
            # print("\nINSERT\n%s\n%s\n" % (statement["sql"], statement["values"]))
            self.cursor.execute(statement["sql"], statement["values"])
            self.conn.commit()
        except psycopg2.errors.UniqueViolation as e:
            logging.warning(f"Query violates unique constraint, entity already exists. {e}")
            if self.get_by_ux_key():
                return True
            return False
        except Exception as e:
            logging.error(f"Error inserting to Postgres: {e}")
            return False
        self.id = self.cursor.fetchone()[0]
        return True

    def update(self) -> bool:
        """Update a model instance by ID, setting the udated time to now."""
        self.updated_ts = arrow.utcnow().datetime
        sql_args = {
            "table_name": self.table_name,
            "set": self._gen_update_set(),
            "where": "id = %s" % self.id
        }
        set_values = self._gen_update_set_parms()
        update_sql = """
            UPDATE %(table_name)s
            SET
            %(set)s
            WHERE
            %(where)s;""" % sql_args
        try:
            self.cursor.execute(update_sql, set_values)
            self.conn.commit()
        except Exception as e:
            logging.critical("Error updating to Postgres: %s" % e)
            return False
        return True

    def delete(self) -> bool:
        """Delete a model instance by ID."""
        if not self.id:
            raise AttributeError("Model %s missing id, cannot be deleted without an ID" % self)
        delete_sql = self._gen_delete_sql_statement()
        try:
            self.cursor.execute(delete_sql, (self.id,))
            self.conn.commit()
        except Exception as e:
            print("Error deleting from Postgres: %s" % e)
            return False
        return True

    def get_by_id(self, _id: int = None) -> bool:
        """Get a model by it's ID."""
        # Check if the field we are requesting by exists within the model.
        if "id" not in self.field_map:
            raise AttributeError("Model: %s missing ID field" % self)
        if not hasattr(self, "id"):
            raise AttributeError("Model: %s missing ID field" % self)
        if not _id and not self.id:
            raise Exception("Missing ID argument")
        if _id:
            search_id = _id
        else:
            search_id = self.id
        fields_str = self._get_field_names_str()
        sql = f"""
            SELECT {fields_str}
            FROM {self.table_name}
             WHERE id = %s;
        """
        self.cursor.execute(sql, (search_id,))
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

    def get_by_name(self, name: str) -> bool:
        """Get a model by it's name."""
        return self.get_by_field(field_name="name", field_value=name)

    def get_by_field(self, field_name: str = None, field_value: str = None) -> bool:
        """Get a model by a field that equals a given value. Check that we have the field in the
        field map and it is set as a class attribute.
        @todo: @psql Figure out how to paramaterize or santize the field name
        """
        if field_name not in self.field_map:
            raise AttributeError(f"Model {self} does not have field: {field_name} in field_map")
        if not hasattr(self, field_name):
            raise Exception(f"Model {self} does not have field: {field_name}")

        fields_str = self._get_field_names_str()
        sql = f"""
            SELECT {fields_str}
            FROM {self.table_name}
            WHERE {field_name} = %s;
            """
        self.cursor.execute(sql, (field_value,))
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

    def get_by_fields(self, fields: list) -> bool:
        """Get a model by a field, or fields.
        :todo: Eventually this needs to support more operators than just eq
        @todo: @psql Figure out how to paramaterize or santize the field name

        :param fields: list of dict
            fields
            [
                {
                    "field": "name",
                    "value": "A Cool Name",
                    "op": "eq"
                }
            ]
        :unit-test: None
        """
        sql_fields = self._gen_get_by_fields_sql(fields)
        fields_str = self._get_field_names_str()
        sql = f"""
            SELECT {fields_str}
            FROM {self.table_name}
            WHERE {sql_fields["sql"]}
            LIMIT 1;"""
        self.cursor.execute(sql, sql_fields["values"])
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

    def get_by_ux_key(self, **kw_args) -> bool:
        """Get a model by it's unique keys. This requires the model to have the self.ux_key field
        set, which is list of field keys that make up a unique key for the table. The kw_args must
        contain values for all the keys for the model.
        """
        if not self.ux_key:
            raise AttributeError("Model: %s has no self.ux_key set." % self)

        logging.info("Attempting to get model by UX key based on model attributes")
        has_fields_ux_field_by_model = True
        for ux_field in self.ux_key:
            if not getattr(self, ux_field):
                has_fields_ux_field_by_model = False
                msg = "Couldnt get model by ux field from model attriubute. Model %s is missing "
                msg += "attribute value for %s"
                logging.warning(msg % (self, ux_field))
                break

        if not has_fields_ux_field_by_model:
            if len(kw_args) != len(self.ux_key):
                msg = "Model has ux key fields: %s, request has %s fields" % (
                    str(self.ux_key), kw_args.keys())
                raise AttributeError(msg)
            self.apply_dict(kw_args)
        where_and = self._gen_where_sql_and(self.ux_key)
        fields_str = self._get_field_names_str()
        sql = f"""
            SELECT {fields_str}
            FROM {self.table_name}
            WHERE {where_and["sql"]}
        """
        # logging.debug(f"\nGET by UX KEY: {sql}\n{kw_args}\n")
        self.cursor.execute(sql, where_and["values"])
        raw = self.cursor.fetchone()
        if raw:
            self.build_from_list(raw)
            return True
        else:
            return False

    def get_last(self) -> bool:
        """Get the last created model."""
        sql = self._gen_get_last_sql()
        self.cursor.execute(sql)
        run_raw = self.cursor.fetchone()
        if not run_raw:
            return False
        self.build_from_list(run_raw)
        return True

    def get_field(self, field_name: str) -> dict:
        """Get the details on a model field from the field map.
        :unit-test: TestApiModelBase::test__get_field
        """
        for fieldmap_name, field in self.field_map.items():
            if field["name"] == field_name:
                return field
        return None

    def _get_field_names_list(self) -> list:
        """Get the model's fields in a lists.
        :unit-test: TestApiModelBase::test__get_field_names_list
        """
        return self.field_map.keys()

    def _get_field_names_str(self) -> str:
        """Get the model's fields in a lists.
        :unit-test: TestApiModelBase::test__get_field_names_str
        """
        return ",".join(self.field_map.keys())

    def build_from_list(self, raw: list) -> bool:
        """Build a model from an ordered list, converting data types to their desired type where
        possible.
        :@todo: Simplify this method, it's too big.
        :param raw: The raw data from the database to be converted to model data.
        :unit-test: TestApiModelBase::test__build_from_list
        """
        if len(self.field_map) != len(raw):
            msg = "BUILD FROM LIST Model: %s field_map: %s, record: %s \n" % (
                self,
                len(self.field_map),
                len(raw))
            msg += "Model Fields:\t\t%s\n" % (self.field_map.keys())
            msg += "Field Map Fields:\t%s\n" % str(self.field_map.keys())
            msg += "Raw Record: %s\n" % str(raw)
            msg += "Maybe .setup() has not been run"
            logging.error(msg)
            raise AttributeError(msg)

        count = 0
        # Probably dont do whats below.
        # self.id = setattr(self, "id", raw[0])
        for field_name, field in self.field_map.items():
            field_name = field['name']
            field_value = raw[count]

            # Handle the bool field type.
            if field['type'] == 'bool':
                if field_value == 1:
                    setattr(self, field_name, True)
                elif field_value == 0:
                    setattr(self, field_name, False)
                else:
                    setattr(self, field_name, None)

            # Handle the datetime field type.
            elif field['type'] == 'datetime':
                if field_value:
                    setattr(self, field_name, arrow.get(field_value).datetime)
                else:
                    setattr(self, field_name, None)

            # Handle the list field type.
            elif field['type'] == 'list':
                if field_value:
                    setattr(self, field_name, field_value)
                else:
                    setattr(self, field_name, None)

            # elif field["type"] == "json":
            #     import ipdb; ipdb.set_trace()
            #     json_value = json.loads(field_value)
            #     setattr(self, field_name, json_value)

            # Handle all other field types without any translation.
            else:
                setattr(self, field_name, field_value)

            count += 1

        return True

    def build_from_dict(self, raw: dict) -> bool:
        """Builds a model by a dictionary. This is expected to be used mostly from a client making
        a request from a web api.
        :unit-test: TestApiModelBase::test__build_from_dict
        """
        for field, value in raw.items():
            if not hasattr(self, field):
                continue

            # if self.field_map[field]["type"] == "datetime":
            #     if isinstance(value, str):
            #         value = date_utils.date_from_json(value)
            setattr(self, field, value)

        return True

    # def sql_value_override_for_model(self, field: dict) -> str:
    #     """Override the SQL value for a field before it's stored into the database.
    #     @todo: determine if this is used.
    #     :unit-test: TestBase::test__sql_value_override_for_model
    #     """
    #     return getattr(self, field["name"])

    def check_required_class_vars(self, extra_class_vars: list = []) -> bool:
        """Quick class var checks to make sure the required class vars are set before proceeding
        with an operation.
        :unit-test: TestBase::test__check_required_class_vars
        """
        if not self.conn:
            raise AttributeError('Missing self.conn')

        if not self.cursor:
            raise AttributeError('Missing self.cursor')

        for class_var in extra_class_vars:
            if not getattr(self, class_var):
                raise AttributeError('Missing self.%s' % class_var)

        return True

    def get_dict(self) -> dict:
        """Get all the model's fields as a dictionary."""
        ret = {}
        for field_name, field_info in self.field_map.items():
            ret[field_name] = getattr(self, field_name)
        return ret

    def apply_dict(self, the_dict: dict) -> bool:
        """Take a dictionary and match the keys and values to the model."""
        if len(the_dict) != len(self.field_map):
            logging.debug(
                "Model %s has %s fields, dict has: %s" % (
                    self, len(self.field_map), len(the_dict)))
        for key, value in the_dict.items():
            if key not in self.field_map:
                logging.warning("Field %s not in model: %s" % (key, self))
                continue
            setattr(self, key, value)
        return True

    def json(self, get_api: bool = False) -> dict:
        """Create a JSON friendly output of the model, converting types to friendlies. If get_api
        is specified and a model doesnt have api_display=False, it will export in the output.
        :unit-test: TestApiModelBase::test__json
        """
        json_out = {}
        for field_name, field in self.field_map.items():
            if get_api and "api_display" in field and not field["api_display"]:
                continue
            value = getattr(self, field["name"])
            if field["type"] == "datetime":
                value = date_utils.json_date(value)
            json_out[field["name"]] = value
        return json_out

    def create_table(self) -> bool:
        """Create an entity table based of a field map."""
        if not hasattr(self, "table_name"):
            raise AttributeError(f"Model {self} has no table_name")
        column_deffs = {
            "id": "SERIAL PRIMARY KEY",
            "created_ts": "TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL",
            "updated_ts": "TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP",
        }
        sql_fields = ""
        for field_name, field_info in self.field_map.items():
            if field_name not in ["id", "created_ts", "updated_ts"]:
                if field_info["type"] == "int":
                    deffinition = "INTEGER"
                if field_info["type"] == "bool":
                    deffinition = "BOOLEAN"
            else:
                deffinition = column_deffs[field_name]
            column_deffs[field_name] = deffinition
            sql_fields += "%s %s,\n" % (field_name, column_deffs[field_name])
        sql_fields = sql_fields[:-2]
        sql = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                {sql_fields}
            );
        """
        print(sql)
        try:
            self.cursor.execute(sql)
            return True
        except Exception as e:
            logging.error("Error creating %s table: %s" % (self, e))
            return False

    def create_table_sql(self) -> str:
        """Generate a create table statement and return it as a string.
        :unit-test: TestApiModelBase::test__create_table_sql
        """
        if not hasattr(self, "table_name"):
            raise AttributeError(f"Model {self} has no table_name")
        column_deffs = {
            "id": "SERIAL PRIMARY KEY",
            "created_ts": "TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL",
            "updated_ts": "TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP",
        }
        field_defs = []
        for field_name, field_info in self.field_map.items():
            if field_name in ["id", "created_ts", "updated_ts"]:
                field_defs.append("\n%s,\n" % column_deffs[field_name])
            else:
                if field_info["type"] == "str":
                    field_type_str = "VARCHAR"
                elif field_info["type"] == "int":
                    field_type_str = "INTEGER"
                elif field_info["type"] == "datetime":
                    field_type_str = "TIMESTAMP"
                elif field_info["type"] == "bool":
                    field_type_str = "BOOLEAN"
                elif field_info["type"] == "list":
                    field_type_str = "TEXT[]"
                else:
                    raise AttributeError(f"Unknown data type: %s {field_info['type']}")
                field_defs.append(f"{field_name} {field_type_str},\n")

        sql = f"CREATE TABLE IF NOT EXISTS {self.table_name}"
        for field_def in field_defs:
            sql += field_def
        sql = sql[:-2]
        return sql

    def _gen_insert_statement(self) -> dict:
        """Generate the insert SQL statement, returning the new generated row's id."""
        insert_segments = self._sql_values()
        insert = {}
        insert["sql"] = f"""
            INSERT INTO {self.table_name}
            ({self._sql_fields()})
            VALUES ({insert_segments["params"]})
            RETURNING id;
        """
        insert["values"] = insert_segments["values"]
        return insert

    def _gen_delete_sql_statement(self) -> str:
        """Generate the delete paramaterized SQL statement.
        :unit-test: TestApiModelBase::test___gen_delete_sql_statement
        """
        delete_sql = f"""
            DELETE FROM {self.table_name}
            WHERE
            id = %s;
        """
        return delete_sql

    # def _gen_insert_sql(self, skip_fields: list = ["id"]) -> tuple:
    #     """Generate the insert SQL statement.
    #     :unit-test: TestApiModelBase::test___gen_insert_sql
    #     """
    #     fields = self._sql_fields_sanitized(skip_fields=skip_fields),
    #     insert_sql = f"INSERT INTO {table_name} ({fields}) VALUES (%s)"
    #     self._sql_insert_values_santized(skip_fields=skip_fields)
    #     return insert_sql

    def _gen_get_by_fields_sql(self, fields: list) -> dict:
        """Generate a str for one or many search fields.
        :param fields: list of dict
            fields
            [
                {
                    "field": "name",
                    "value": "A Cool Name",
                    "op": "eq"
                }
            ]
        :returns: {
            "sql": "name = %s AND color = %s",      A paramaterized field comparassion
            "values": ()                            Tuple with the values to paramaterize
        }
        :unit-test: TestApiModelBase::test___gen_get_by_fields_sql
        """
        sql_fields = {
            "sql": "",
            "values": []
        }
        for field in fields:
            if not field["value"]:
                operation = "IS"
            # elif field["type"] == "list":
            #     operation = "IN"
            elif field["op"] in ["eq", "="]:
                operation = "="
            else:
                logging.error("Unanticipated operation value: %s for model: %s" % (
                    field["op"],
                    self))
                
            field_qry = f"{field['field']} {operation} %s AND "
            sql_fields["sql"] += field_qry

            value = self._sql_field_value(self.field_map[field["field"]], field)
            sql_fields["values"].append(value)
        sql_fields["sql"] = sql_fields["sql"][:-4]
        sql_fields["values"] = tuple(sql_fields["values"])
        return sql_fields

    def _gen_get_last_sql(self) -> str:
        """Generate the last created row SQL.
        :unit-test: TestApiModelBase::test___gen_get_last_sql
        """
        fields_str = self._get_field_names_str()
        sql = f"""
            SELECT {fields_str}
            FROM {self.table_name}
            ORDER BY created_ts DESC
            LIMIT 1;
        """
        return sql

    def _sql_field_value(self, field_map_info: dict, field_data: dict) -> str:
        """Get the correctly typed value for a field, santized and ready for use in SQL.
        @todo: @psql Investigate how this changes with psql paramaterization.
        :unit-test: TestApiModelBase::test___sql_field_value
        """
        if field_data["value"] is None:
            return "NULL"

        # # Handle bools
        # elif field_map_info["type"] == "bool":
        #     if field_data["value"] == True:
        #         value = 1
        #     elif field_data["value"] == False:
        #         value = 0
        #     else:
        #         logging.error("Unanticipated bool value: %s for model: %s" % (
        #             field_data["value"],
        #             self))
        #         return False

        # Handle lists
        # if field_map_info["type"] == "list":
        #     value = '("%s")' % sql_tools.sql_safe(field_data["value"])
        #     raise NotImplementedError("Have not implemented storing list data types yet.")
        if field_map_info["type"] == "json":
            raise NotImplementedError("Have not implemented storing json data types yet.")

        # Handle str and everything else
        else:
            value = field_data["value"]

        return value

    def _sql_fields(self) -> str:
        """Get all the required SQL fields for a given SQL operation.
        :unit-test: TestApiModelBase::test___sql_fields
        """
        fields = ""
        for field_name, field in self.field_map.items():
            if field_name in self.skip_fields:
                continue
            fields += "%s, " % field_name
        if fields:
            return fields[:-2]
        return ""

    def _sql_values(self) -> dict:
        """Creates the values portion of a query with the actual values sanitized.
        example:
        :unit-test: TestApiModelBase::test___sql_values
        """
        values = []
        value_data = self._get_values_sql_typed()
        params = ""
        for field_name, field in self.field_map.items():
            if field["name"] in self.skip_fields:
                continue
            value = value_data[field_name]
            values.append(value)
            params += "%s, "
        params = params[:-2]
        return {
            "params": params,
            "values": tuple(values)
        }

    def _gen_update_set(self) -> str:
        """Generate the SET portion of a SQL query."""
        skip_fields = ["id", "created_ts"]
        set_sql = ""
        for field_name, field in self.field_map.items():
            # Skip fields we don't want included in db writes
            if field['name'] in skip_fields:
                continue
            set_sql += field['name'] + "=%s, "
        set_sql = set_sql[:-2]
        return set_sql

    def _gen_update_set_parms(self) -> tuple:
        """Generate the the values for the UPDATE statement."""
        skip_fields = ["id", "created_ts"]
        set_values = []
        for field_name, field in self.field_map.items():
            # Skip fields we don't want included in db writes
            if field['name'] in skip_fields:
                continue
            set_values.append(getattr(self, field_name))
        return tuple(set_values)

    def _gen_where_sql_and(self, fields: list) -> dict:
        """Generate the portion of a where clause for any query requiring a WHERE statemnt.
        """
        sql = ""
        values = []
        value_info = self._get_values_sql_typed()
        for field_name in fields:
            sql += f"{field_name} = %s AND "
            value = value_info[field_name]
            values.append(value)
        sql = sql[:-4]
        return {
            "sql": sql,
            "values": tuple(values)
        }

    def _get_values_sql_typed(self):
        data = {}
        for field_name, field_info in self.field_map.items():
            value = getattr(self, field_name)

            # Convert a Date value
            if field_info["type"] == "date":
                if isinstance(value, arrow.Arrow):
                    value = value.date()
                elif isinstance(value, datetime) or isinstance(value, date):
                    value = arrow.get(value).date()

            # Convert a Datetime value
            elif field_info["type"] == "datetime":
                if isinstance(value, arrow.Arrow):
                    value = value.datetime

            # Attempt to convert a python dict as json.
            elif field_info["type"] == "json":
                try:
                    value = json.dumps(value)
                except Exception as e:
                    logging.error("Cannot parse json field %s as json. %s. Data: %s" % (
                        field_name,
                        e,
                        value))
                    raise e
            data[field_name] = value
        return data

    def _set_defaults(self) -> bool:
        """Set the defaults for the class field vars and populates the self.field_list var
        containing all table field names.
        :unit-test: TestApiModelBase::test___set_defaults
        """
        self.field_list = []
        for field_name, field in self.field_map.items():
            field_name = field['name']
            self.field_list.append(field_name)

            default = None
            
            if 'default' in field:
                default = field['default']

            # Sets all class field vars with defaults.
            field_value = getattr(self, field_name, None)
            if field_value:
                continue

            if field["type"] == "bool":
                if field_value == False:
                    setattr(self, field_name, False)
                elif field_value:
                    setattr(self, field_name, True)
                else:
                    setattr(self, field_name, default)
            elif field["type"] == "list":
                setattr(self, field_name, [])
            elif not field_value:
                setattr(self, field_name, default)
            else:
                setattr(self, field_name, None)

        return True

    def _set_types(self) -> bool:
        """Set the types of class table field vars and corrects their types where possible.
        :unit-test: TestApiModelBase::test___set_types
        """
        for field_name, field in self.field_map.items():
            class_var_name = field['name']

            class_var_value = getattr(self, class_var_name)
            if class_var_value is None:
                continue

            if field['type'] == 'int' and type(class_var_value) is not int:
                converted_value = xlate.convert_any_to_int(class_var_value)
                setattr(self, class_var_name, converted_value)
                continue

            if field['type'] == 'bool':
                converted_value = xlate.convert_int_to_bool(class_var_value)
                setattr(self, class_var_name, converted_value)
                continue

            if field['type'] == 'datetime' and type(class_var_value) not in [datetime, date]:
                setattr(
                    self,
                    class_var_name,
                    self._get_datetime(class_var_value))
                continue

    def _generate_create_table_feilds(self) -> str:
        """Generates all fields column create sql statements.
        """
        field_sql = ""
        field_num = len(self.field_map)
        c = 1
        for field_name, field in self.field_map.items():
            if field["type"] == "unique_key":
                continue
            primary_stmt = ''
            if 'primary' in field and field['primary']:
                primary_stmt = ' PRIMARY KEY'
                if self.backend == "mysql":
                    primary_stmt += ' AUTO_INCREMENT'
            if "extra" in field:
                primary_stmt = " %s" % field["extra"]

            not_null_stmt = ''
            if 'not_null' in field and field['not_null']:
                not_null_stmt = ' NOT NULL'

            default_stmt = ''
            if 'default' in field and field['default']:
                if field['type'] == "str":
                    default_stmt = ' DEFAULT "%s"' % field['default']
                elif field["type"] == "list":
                    default_stmt = ' DEFAULT "%s"' % ",".join(field['default'])
                else:
                    default_stmt = ' DEFAULT %s' % field['default']

            field_line = "`%(name)s` %(type)s%(primary_stmt)s%(not_null_stmt)s%(default_stmt)s," % {
                'name': field['name'],
                'type': self._xlate_field_type(field['type']),
                'primary_stmt': primary_stmt,
                'not_null_stmt': not_null_stmt,
                'default_stmt': default_stmt
            }
            field_sql += field_line

            if c == field_num:
                field_sql = field_sql[:-1]
            field_sql += "\n"
            c += 1

        for field_name, field in self.field_map.items():
            if field["type"] == "unique_key":
                field_sql += "UNIQUE KEY %s (%s)" % (field["name"], ",".join(field["fields"]))
        field_sql = field_sql[:-1]
        return field_sql

    def _xlate_field_type(self, field_type: str) -> str:
        """Translates field types into sql lite column types.
        @todo: create better class var for xlate map.
        @todo @psql: Update this for postgres
        :unit-test: TestApiModelBase.test___xlate_field_type
        """
        if self.backend == "psql":
            if field_type == 'int':
                return 'INTEGER'
            elif field_type == 'datetime':
                return 'DATETIME'
            elif field_type[:3] == 'str':
                return 'VARCHAR(200)'
            elif field_type == 'text':
                return "TEXT"
            elif field_type == 'bool':
                return 'TINYINT(1)'
            elif field_type == 'float':
                return 'DECIMAL(10, 5)'
            elif field_type == 'list':
                return "TEXT"
            elif field_type == "json":
                return "JSON"
            else:
                raise AttributeError(f'Unknown data type: "{field_type}"')

    def _establish_db(self, conn, cursor) -> bool:
        """Store the database connection as class vars.
        :unit-test: TestApiModelBase.test___establish_db
        """
        self.conn = conn
        if not self.conn and "conn" in glow.db:
            self.conn = glow.db["conn"]
        self.cursor = cursor
        if not self.cursor and "cursor" in glow.db:
            self.cursor = glow.db["cursor"]
        return True

    def _is_model_json(self) -> bool:
        """Check if a model contains a JSON field type, if it does, return True.
        :unit-test: TestApiModelBase:test___is_model_json
        """
        for field_name, field_info in self.field_map.items():
            if field_info["type"] == "json":
                return True
        return False

    def _get_datetime(self, date_string: str) -> datetime:
        """Attempt to get a Python native datetime from a date string.
        :unit-test: TestApiModelBase:test____get_datetime
        """
        if isinstance(date_string, arrow.Arrow):
            return date_string.datetime
        if len(date_string) == 26:
            try:
                parse_format = "YYYY-MM-DD HH:mm:ss ZZ"
                parsed_date = arrow.get(date_string, parse_format)
                return parsed_date.datetime
            except arrow.parser.ParserMatchError:
                logging.error("Couldnt parse date str: %s with with format: %s" % (
                    date_string,
                    parse_format))
        elif len(date_string) == 19:
            try:
                parse_format = "YYYY-MM-DD HH:mm:ss"
                parsed_date = arrow.get(date_string, parse_format)
                return parsed_date.datetime
            except arrow.parser.ParserMatchError:
                logging.error("Couldnt parse date str: %s with format: %s " % (
                    date_string,
                    parse_format))
        else:
            try:
                parsed_date = arrow.get(date_string)
                return parsed_date.datetime
            except arrow.parser.ParserMatchError:
                logging.error("Couldnt parse date str: %s" % date_string)
                return None
            except arrow.parser.ParserError:
                logging.error("Couldnt parse date str: %s" % date_string)
                return None

# End File: politeauthority/bookmarky-api/src/bookmarky/api/models/base.py
