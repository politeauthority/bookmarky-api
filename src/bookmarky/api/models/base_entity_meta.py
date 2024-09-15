"""
    Cver Api - Model
    Base Entity Meta Model
    Base model class for all models requiring meta storage.

"""
import logging

from bookmarky.api.models.base import Base
from bookmarky.api.models.entity_meta import EntityMeta


class BaseEntityMeta(Base):

    def __init__(self, conn=None, cursor=None):
        """Base Entity Meta model constructor."""
        super(BaseEntityMeta, self).__init__(conn, cursor)
        self.table_name = None
        self.table_name_meta = EntityMeta().table_name
        self.metas = {}

    def __repr__(self):
        if self.id:
            return "<%s: %s>" % (self.__class__.__name__, self.id)
        return "<%s>" % self.__class__.__name__

    def get_by_id(self, model_id: int) -> bool:
        """Get a single model object from db based on an object ID with all meta data loaded into
           self.metas.
        """
        if not super(BaseEntityMeta, self).get_by_id(model_id):
            return False
        self.load_meta()
        return True

    def build_from_list(self, raw: list, meta=False) -> bool:
        """Build a model from list, and pull its meta data."""
        super(BaseEntityMeta, self).build_from_list(raw)
        if meta:
            self.load_meta()

    def build_from_dict(self, raw: dict) -> bool:
        """Builds a model by a dictionary. This is expected to be used mostly from a client making
        a request from a web api.
        This extends the original to unpack meta objects.
        """
        super(BaseEntityMeta, self).build_from_dict(raw)
        if 'meta' not in raw:
            return True

        for meta_key, meta_value in raw["meta"].items():
            self.meta[meta_key] = meta_value

        return True

    def save(self) -> bool:
        """Extend the Base model save, settings saves for all model self.metas objects.
        @todo: This needs some work, we're having trouble getting the correct value stored.
        """
        super(BaseEntityMeta, self).save()
        if not self.metas:
            return True

        if not self.id:
            raise AttributeError('Model %s cant save entity metas with out id' % self)

        existing_meta = self.load_meta(set_values=False)
        for meta_name, meta_value in self.metas.items():
            if not isinstance(meta_value, EntityMeta):
                meta = EntityMeta()
                meta.name = meta_name
                meta.value = str(meta_value)
            else:
                meta.value = meta_value
            if hasattr(self, "user_id"):
                meta.user_id = self.user_id
            else:
                logging.error("Model {self} does not have a user_id attribute!")

            if existing_meta and meta_name in existing_meta:
                meta.id = existing_meta[meta_name].id
                meta.user_id = existing_meta[meta_name].user_id

            meta.entity_type = self.table_name
            meta.entity_id = self.id
            if not meta.type:
                meta.type = 'str'

            meta.save()
            self.metas[meta_name] = meta
        return True

    def delete(self) -> bool:
        """Delete a model item and it's meta."""
        super(BaseEntityMeta, self).delete()
        sql = f"""
            DELETE FROM {self.table_name_meta}
            WHERE
                entity_id = %s AND
                entity_type = %s
            """
        self.cursor.execute(sql, (self.id, self.table_name))
        self.conn.commit()
        return True

    def get_meta(self, meta_name: str):
        """Get a meta key from an entity if it exists, or return None. """
        if meta_name not in self.metas:
            return False
        else:
            return self.metas[meta_name]

    def meta_update(self, meta_name: str, meta_value, meta_type: str = 'str') -> bool:
        """Set a models entity value if it currently exists or not."""
        if meta_name not in self.metas:
            self.metas[meta_name] = EntityMeta(self.conn, self.cursor)
            self.metas[meta_name].name = meta_name
            self.metas[meta_name].type = meta_type
        self.metas[meta_name].value = meta_value
        return True

    def load_meta(self, set_values: bool = True) -> dict:
        """Load the model's meta data. Setting the meta values to the instance if requested, and
        returning the meta values as a dict.
        """
        sql = f"""
            SELECT *
            FROM {self.table_name_meta}
            WHERE
                entity_id = %s AND
                entity_type = %s;
            """
        logging.debug("\nLOADED METAS")

        self.cursor.execute(sql, (self.id, self.table_name))
        meta_raws = self.cursor.fetchall()
        print(meta_raws)
        logging.debug("\nEND LOADED METAS\m")
        print("Loading meta data")
        metas = self._load_from_meta_raw(meta_raws)
        if set_values:
            self.metas = metas
        return metas

    def _load_from_meta_raw(self, meta_raws) -> dict:
        """Create self.metas for an object from raw_metas data."""
        ret_metas = {}
        for meta_raw in meta_raws:
            em = EntityMeta(self.conn, self.cursor)
            em.build_from_list(meta_raw)
            ret_metas[em.name] = em
        return ret_metas
        # self.metas = ret_metas


# End File: pignus/src/pignus_api/models/base_entity_meta.py
