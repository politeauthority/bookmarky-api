"""
    Bookmarky Api
    Collects - Base

    Testing:
        Unit test file  bookmarky/tests/unit/api/collects/test_base.py
        Unit tested     10/25

"""

import logging
import math

from bookmarky.api.utils import glow
from bookmarky.api.utils import sql_tools


class Base:

    def __init__(self, conn=None, cursor=None):
        """Class constructor, set the db connection vars.
        :unit-test: TestApiCollectsBase.test____init__
        """
        self.conn = conn
        if not self.conn:
            self.conn = glow.db["conn"]
        self.cursor = cursor
        if not self.cursor:
            self.cursor = glow.db["cursor"]
        self.table_name = None
        self.collect_model = None
        self.per_page = 20
        self.field_map = {}
        if self.collect_model:
            self.field_map = self.collect_model().field_map

    def build_from_lists(self, raws: list) -> list:
        """Creates list of hydrated collection objects."""
        prestines = []
        for raw_item in raws:
            new_object = self.collect_model(self.conn, self.cursor)
            new_object.build_from_list(raw_item)
            prestines.append(new_object)
        return prestines

    def get_all(self) -> list:
        """Get all units.
        @note: This should be used sparingly as it has no limits.
        """
        msg = "Use this method: collect_base.basebase().get_all() sparingling as it hasno limit"
        msg += "on the query"
        logging.warning(msg)
        sql = """SELECT * FROM %s;""" % self.table_name
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        if not raws:
            return []
        presitines = self.build_from_lists(raws)
        return presitines

    def get_by_ids(self, the_ids: list) -> list:
        """Get all models that match the ids provided."""
        # the_ids = ""
        # for an_id in ids:
        #     the_ids += "%s," % an_id
        # the_ids = the_ids[:-1]
        sql_ids = []
        for an_id in the_ids:
            sql_ids.append(an_id)

        if len(sql_ids) == 1:
            w_query = " id = %s"
            w_values = tuple(sql_ids[0],)
        else:
            w_query = " id IN %s"
            w_values = tuple(sql_ids)
            # w_values = "id IN %s"

        sql = f"""
            SELECT *
            FROM {self.table_name}
            WHERE"""
        sql += w_query

        try:
            self.cursor.execute(sql, (w_values,))
        except Exception as e:
            # print(w_query)
            print(e)
            # logging.critical("SQL error: %s\n" (
            #     str(e),
            #     # self.cursor.mogrify(sql, (w_query))
            # ))
        raws = self.cursor.fetchall()
        if not raws:
            return []
        presitines = self.build_from_lists(raws)
        return presitines

    def get_count_all(self) -> int:
        sql = """SELECT count(*) FROM %s;""" % self.table_name
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return 0
        return raw[0]

    def load_presiteines(self, raws: list) -> list:
        if not raws:
            return []
        return self.build_from_lists(raws)

    def make_keyed(self, records: list, key_field: str) -> dict:
        """Translate a list of of models into a dictionary keyed by the supplied field.
        :Warning: This does not properly protect against non unique key_fields yet.
        """
        if key_field not in self.collect_model().field_map:
            raise AttributeError("Model: %s does not have field: %s" % (
                self.collect_model, key_field))
        ret_dict = {}
        for record in records:
            the_key = getattr(record, key_field)
            if the_key in ret_dict:
                logging.warning("Key: %s already exists in ret_dict for model: %s " % (
                    the_key, self.collect_model))
            ret_dict[getattr(record, key_field)] = record
        return ret_dict

    def get_paginated(
        self,
        page: int = 1,
        limit: int = 0,
        user_limit: int = None,
        order_by: dict = {},
        where_and: list = [],
        per_page: int = 20,
        get_json: bool = False,
        get_api: bool = False
    ) -> list:
        """
        Get paginated collection of models.
        :param limit: The limit of results per page.
        :param user_limit: A user imposed limit that sits outside of the api's limit restrictions.
        :param offset: The offset to return pages from or the "page" to return.
        :param order_by: A dict with the field to us, and the direction of the order.
            example value for order_by:
            {
                'field': 'last_seen',
                'op' : 'DESC'
            }
        :param where_and: a list of dictionaries, containing fields, values and the operator of AND
            statements to concatenate for the query.
            example value for where_and:
            [
                {
                    'field': 'last_seen',
                    'value': last_online,
                    'op': '>='
                }
            ]
        :returns: A list of model objects, hydrated to the default of the base.build_from_list()
        """
        if limit == 0:
            limit = per_page
        query = self._generate_paginated_sql(page, where_and, order_by, limit)
        log_msg = "\nPAGINATIED SQL\n \nMETHOD:get_paginatd\n"
        log_msg += f"PARAMS:\n\tWHERE AND:{where_and}"
        log_msg += f"{query['sql']}\n{query['params']}\n\n"
        logging.debug(log_msg)
        self.cursor.execute(query["sql"], query["params"])
        raw = self.cursor.fetchall()
        prestines = []
        for raw_item in raw:
            new_object = self.collect_model(self.conn, self.cursor)
            new_object.build_from_list(raw_item)
            prestines.append(new_object)
        if get_json:
            json_prestines = []
            for prestine in prestines:
                json_prestines.append(prestine.json(get_api))
            prestines = json_prestines

        ret = {
            'objects': prestines,
            'info': self.get_pagination_info(query, page, limit, user_limit)
        }
        if get_json:
            ret["info"]["object_type"] = self.collect_model.model_name
        return ret

    def get_pagination_info(
            self,
            query: dict,
            current_page: int,
            per_page: int,
            user_limit: int = None
    ) -> dict:
        """Get pagination details, supplementary info from the get_paginated method. This contains
        details like total_objects, next_page, previous page and other details needed for properly
        drawing pagination info on a GUI.
        :param query: A diction containing the SQL parameterized and key of "values" that contains
            the query values
        """
        total_objects = self._pagination_total(query, user_limit)
        last_page = math.ceil(total_objects / per_page)
        if last_page == 0:
            last_page = 1
        ret = {
            "total_objects": total_objects,
            "current_page": current_page,
            "last_page": last_page,
            "per_page": per_page,
        }
        return ret

    def _generate_paginated_sql(
        self,
        page: int,
        where_and: list,
        order_by: dict,
        limit: int,
    ) -> dict:
        """Generate the SQL query for the paginated request.
        :unit-test: TestApiCollectsBase::test___generate_paginated_sql()
        """
        where = self._pagination_where_and(where_and)
        sql_vars = {
            "table_name": self.table_name,
            "where": where["sql"],
            "order": self._pagination_order(order_by),
            "limit": self._gen_pagination_limit_sql(limit),
            "offset": ""
        }
        if sql_vars["limit"]:
            sql_vars["offset"] = self._gen_pagination_offset_sql(page, limit)
        sql = """
            SELECT *
            FROM %(table_name)s
            %(where)s
            %(order)s
            %(limit)s%(offset)s;""" % sql_vars
        ret = {
            "sql": sql,
            "params": tuple(where["params"])
        }
        # logging.info("\n\nRaw SQL\n%s\n" % sql)
        return ret

    def _pagination_total(self, query: dict, user_limit: int = None) -> int:
        """Get the total number of pages for a pagination query.
        :param query: A diction containing the SQL parameterized and key of "values" that contains
            the query values
        """
        total_sql = self._edit_pagination_sql_for_info(query, user_limit)
        # logging.info("PAGINATION INFO SQL:\n%s" % total_sql)
        self.cursor.execute(total_sql, query["params"])
        raw = self.cursor.fetchone()
        if not raw:
            return 0
        count = raw[0]
        if not user_limit:
            return count
        if count > user_limit:
            return user_limit
        return count

    def _edit_pagination_sql_for_info(self, query: dict, user_limit: int = None):
        """Edit the original pagination query to get the total number of results for pagination
        details.
        :param query: A diction containing the SQL parameterized and key of "values" that contains
            the query values
        :unit-test: TestBase::test___edit_pagination_sql_for_info
        """
        original_sql = query["sql"]
        sql = original_sql[original_sql.find("FROM"):]
        sql = "%s %s" % ("SELECT COUNT(*)", sql)
        end_sql = sql.find(" ORDER BY")
        sql = sql[:end_sql].strip()
        if user_limit:
            sql += " LIMIT %s" % user_limit
        sql += ";"
        return sql

    def _pagination_where_and(self, where_and: list) -> dict:
        """Create the where clause for pagination when where and clauses are supplied.
        Note: We append multiple statements with an AND in the sql statement.
        :param where_and:
            example: [
                {
                    "field": "name",
                    "value": "test",
                    "op": "="
                }
            ]
        :unit-test: TestBase::test___pagination_where_and()
        """
        where = False
        where_and_sql = ""

        params = []
        for where_a in where_and:
            one_where_a_sql = self._pagination_where_and_one(where_a)
            if one_where_a_sql:
                where = True
            where_and_sql += one_where_a_sql["sql"]
            params.append(one_where_a_sql["param"])

        if where:
            where_and_sql = "WHERE " + where_and_sql
            where_and_sql = where_and_sql[:-4]
        ret = {
            "sql": where_and_sql,
            "params": params
        }
        return ret

    def _pagination_where_and_one(self, where_a: dict) -> dict:
        """Handles a single field's where and SQL statemnt portion.
        Note: We append multiple statements with an AND in the sql statement.
        @todo: This should be more parameterized
        """
        where_and_sql = ""
        if not where_a["field"]:
            logging.warning("Collections - Invalid where option: %s" % where_a)
            return ""

        op = "="
        if "op" in where_a:
            op = where_a["op"]
        # if "op" not in ["=", "<", ">"]:
        #     op = "="
        if not self.collect_model:
            raise AttributeError("Model %s does not have a collect_model." % self)

        if not self.collect_model().field_map:
            raise AttributeError("%s model ." % self)

        if where_a["field"] not in self.field_map:
            raise AttributeError("Model %s does not have field: %s" % (
                self,
                where_a["field"]))
        where_and_sql += f"{sql_tools.sql_safe(where_a['field'])} {op} %s AND "
        ret = {
            "sql": where_and_sql,
            "param": where_a["value"]
        }
        return ret

    def _pagination_order(self, order: dict = None) -> str:
        """Create the order clause for pagination using user supplied arguments or defaulting to
        created_desc DESC.
        @todo: Make this more paramaterized
        :param order: The ordering dict
            example: {
                "field": "id"
                "direction": "DESC"
            }
        :unit-test: TestBase::test___pagination_order
        """
        order_sql = "ORDER BY created_ts DESC"
        if not order:
            return order_sql
        order_field = order['field']
        if "direction" not in order:
            order_direction = "ASC"
        else:
            order_direction = order['direction']
        order_sql = 'ORDER BY %s %s' % (
            sql_tools.sql_safe(order_field),
            sql_tools.sql_safe(order_direction))
        return order_sql

    def _gen_pagination_limit_sql(self, limit: int) -> str:
        """Get the pagination limit, based on model limit restrictions and user requested limits
        created_desc DESC.
        :unit-test: TestBase::test___gen_pagination_limit_sql
        """
        if isinstance(limit, int):
            return "LIMIT %s" % limit
        logging.warning("No value for query limit")
        return ""

    def _gen_pagination_offset_sql(self, page: int, limit: int) -> str:
        """Get the pagination offset sql value
        """
        return " OFFSET %s" % self._pagination_offset(page, limit)

    def _pagination_offset(self, page: int, per_page: int) -> int:
        """Get the offset number for pagination queries.
        :unit-test: TestBase.test___pagination_offset
        """
        if page == 1:
            offset = 0
        else:
            offset = (page * per_page) - per_page
        return offset

    def _int_list_to_sql(self, item_list: list) -> str:
        """Transform a list of ints to a sql safe comma separated string.
        :unit-test: TestApiCollectsBase::test___int_list_to_sql
        """
        sql_ids = ""
        for i in item_list:
            sql_ids += "%s," % sql_tools.sql_safe(i)
        sql_ids = sql_ids[:-1]
        return sql_ids

    def _get_previous_page(self, page: int) -> int:
        """Get the previous page, or first page if below 1.
        :unit-test: TestBase.test___get_previous_page
        """
        if page == 1:
            return None
        previous = page - 1
        return previous

    def _get_next_page(self, page: int, last_page: int) -> int:
        """Get the next page.
        :unit-test: TestBase::test___get_next_page
        """
        if page == last_page:
            return None
        next_page = page + 1
        return next_page

    def _gen_sql_get_last(self) -> str:
        """Generate the get last SQL statement.
        :unit-test: TestApiCollectsBase:test___gen_sql_get_last
        @todo: update what ever is using this, the psql change updated this a lot @tag: psql
        """
        sql = f"""
            SELECT *
            FROM {self.table_name}
            ORDER BY created_ts DESC
            LIMIT %s;"""
        return sql

    # def _gen_get_by_ids_sql(self) -> str:
    #     """Generate the get_by_ids SQL statement.
    #     :method: TestApiCollectsBase::test___gen_sql_get_last
    #     @todo: fix what's using this as we've made it paramaterized. @tag: psql
    #     """
    #     # model_ids = list(set(model_ids))
    #     # sql_ids = self._int_list_to_sql(model_ids)
    #     sql = f"""
    #         SELECT *
    #         FROM {self.table_name}
    #         WHERE id IN %s;"""
    #     return sql

# End File: politeauthority/bookmarky/src/bookmarky/api/collections/base.py
