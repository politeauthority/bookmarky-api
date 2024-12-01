"""
    Bookmarky Api
    Collection
    Base Entity Metas

This class should be extended by all collections that collect models that have entity meta.

"""
import logging

from bookmarky.api.collects.base import Base
from bookmarky.api.models.entity_meta import EntityMeta


class BaseEntityMetas(Base):

    def __init__(self, conn=None, cursor=None):
        """Base collection constructor. var `table_name must be the """
        super(BaseEntityMetas, self).__init__(conn, cursor)
        self.table_name = None
        self.collect_model = None
        self.meta_table = 'entity_metas'

    def build_from_lists(self, raws: list, meta: bool = False) -> list:
        """Creates list of hydrated collection objects, optionally loading the entities meta
           values.
        """
        prestines = []
        for raw_item in raws:
            new_object = self.collect_model(self.conn, self.cursor)
            new_object.build_from_list(raw_item, meta=meta)
            prestines.append(new_object)
        return prestines

    def get_with_meta_key(self, meta_name: str) -> list:
        """Collect models with a meta key. """
        sql = """
            SELECT *
            FROM `%s`
            WHERE
                entity_type = "%s" AND
                name = "%s"
        """ % (self.meta_table, self.table_name, meta_name)
        self.cursor.execute(sql)

        metas_raw = self.cursor.fetchall()
        prestines = []
        for meta_raw in metas_raw:
            meta = EntityMeta(self.conn, self.cursor)
            meta.build_from_list(meta_raw)
            model = self.collect_model(self.conn, self.cursor)
            model.get_by_id(meta.entity_id)
            prestines.append(model)
        return prestines

    def get_with_meta_value(self, meta_name: str, meta_value) -> list:
        """Collect models with a meta key and value."""
        sql = """
            SELECT *
            FROM %s
            WHERE
                entity_type = "%s" AND
                name = "%s" AND
                value = "%s"
        """ % (self.meta_table, self.table_name, meta_name, meta_value)
        self.cursor.execute(sql)
        metas_raw = self.cursor.fetchall()
        prestines = []
        for meta_raw in metas_raw:
            meta = EntityMeta(self.conn, self.cursor)
            meta.build_from_list(meta_raw)
            model = self.collect_model(self.conn, self.cursor)
            model.get_by_id(meta.entity_id)
            prestines.append(model)
        return prestines

    def get_entities_without_meta_key(self, meta_name: str) -> list:
        """Collect models that do not have a given a meta key. """
        # select_fields = self.
        select_fields = self._get_field_names_str("b")
        sql = f"""
            SELECT {select_fields}
            FROM {self.table_name} as b
                LEFT JOIN {self.meta_table} as em
                    ON
                        b.id = em.entity_id AND
                        em.entity_type = '{self.table_name}' AND
                        em.name = %s;
        """
        logging.info("\n\n")
        self.cursor.mogrify(sql, (meta_name,))
        logging.info(sql)
        logging.info("\n\n")
        self.cursor.execute(sql, (meta_name,))
        entities_raw = self.cursor.fetchall()
        return self.load_presiteines(entities_raw)

    def get_paginated(
        self,
        page: int = 1,
        limit: int = 0,
        user_limit: int = None,
        order_by: dict = {},
        where_and: list = [],
        where_or: list = [],
        per_page: int = 20,
        get_json: bool = False,
        get_api: bool = False
    ) -> list:
        """
        Get paginated collection of models.
        This will also collect the Entity Metas for all results of the pagination query.

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
        logging.debug("\n\nHERES THE NEW META PAGINATION")
        paginated = super(BaseEntityMetas, self).get_paginated(
            page, limit, user_limit, order_by, where_and, where_or, per_page, get_json, get_api)
        logging.debug("@note: Here's where we left off")
        return paginated

    def get_metas_for_entities(self, entity_type: str, entities: list) -> list:
        """From a hydraded list of entities, get the EntityMeta data for each Entity and attatch it
        to the returned result.
        :param entity_type:
        """
        if not entities:
            return []
        # entity_ids = self.gen_entity_ids(entities)
        # sql = """
        #     SELECT *
        #     FROM entity_metas em
        #     WHERE
        #         em.entity_type = %s AND
        #         em.entity_id IN %s;
        # """
        # logging.debug("Loading entity meta for a collection")
        # logging.debug(self.cursor.mogrify(sql, (entity_type, entity_ids)))
        # self.cursor.execute(sql, (entity_type, entity_ids))
        # metas_raw = self.cursor.fetchall()
        return entities

    def gen_entity_ids(self, entities: list):
        ret_ids = []
        for entity in entities:
            ret_ids.append(entity.id)
        return tuple(ret_ids)

# End File: politeauthority/bookmarky-api/src/bookmarky/api/collects/base_entity_metas.py
