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
            self.metas[meta_name] = self._save_single_meta(existing_meta, meta_name, meta_value)

        return True

    def json(self, get_api: bool = False) -> dict:
        """Create a JSON friendly output of the model, converting types to friendlies. If get_api
        is specified and a model doesnt have api_display=False, it will export in the output.
        We extend the Base model's json method and make sure that we also turn the meta fields into
        json friendly output.
        """
        json_out = super(BaseEntityMeta, self).json()
        if not self.metas:
            return json_out
        for meta_key, meta in self.metas.items():
            if isinstance(meta, EntityMeta):
                if "metas" not in json_out:
                    json_out["metas"] = {}
                json_out["metas"][meta_key] = meta.json()
            else:
                logging.error("Entity {self} meta key {meta_key} not not instance of EntityMeta")
                continue
        return json_out

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
        self.cursor.execute(sql, (self.id, self.table_name))
        meta_raws = self.cursor.fetchall()
        logging.debug("Loading meta data for {self}")
        metas = self._load_from_meta_raw(meta_raws)
        if set_values:
            self.metas = metas
        return metas

    def _load_from_meta_raw(self, meta_raws) -> dict:
        """Load meta data from the database, returning it as a dictionary"""
        ret_metas = {}
        for meta_raw in meta_raws:
            em = EntityMeta(self.conn, self.cursor)
            em.build_from_list(meta_raw)
            ret_metas[em.name] = em
        return ret_metas
        # self.metas = ret_metas

    def _save_single_meta(self, existing_meta, meta_name, meta_value) -> EntityMeta:
        """Save a single meta field."""
        if meta_name not in self.field_map_metas:
            logging.error(f"Model {self} does not allow meta key {meta_name}")
            return False
        meta_desc = self.field_map_metas[meta_name]
        if not isinstance(meta_value, EntityMeta):
            meta = EntityMeta()
            meta.name = meta_name
            meta.value = str(meta_value)
        else:
            meta.value = meta_value
        if hasattr(self, "user_id"):
            meta.user_id = self.user_id
        elif hasattr(self, "user_id_field"):
            meta.user_id = getattr(self, "user_id_field")
        else:
            error_msg = f"Model {self} does not have a user identification attribute! Failed to "
            error_msg += f"save meta key: {meta_name}"
            logging.error(error_msg)

        if existing_meta and meta_name in existing_meta:
            meta.id = existing_meta[meta_name].id
            meta.user_id = existing_meta[meta_name].user_id

        meta.entity_type = self.table_name
        meta.entity_id = self.id
        meta.type = meta_desc["type"]

        if meta.save():
            return meta
        else:
            logging.error("Failed to save meta")
            return False

# End File: politeauthority/bookmarky-api/src/bookmarky/models/base_entity_meta.py
