"""
    Bookmarky Api
    Model - Tag

"""
from polite_lib.utils import xlate

from bookmarky.shared.models.tag import FIELD_MAP, FIELD_META
from bookmarky.api.models.base_entity_meta import BaseEntityMeta


class Tag(BaseEntityMeta):

    model_name = "tag"

    def __init__(self, conn=None, cursor=None):
        """Create the instance.
        :unit-test: TestApiModelApiKey::test____init__
        """
        super(Tag, self).__init__(conn, cursor)
        self.field_map = FIELD_MAP
        self.ux_key = FIELD_META["ux_key"]
        self.table_name = "tags"
        self.immutable = True
        self.createable = True
        self.setup()

    def __repr__(self):
        """Tag model representation."""
        if self.name:
            return "<%s: %s - %s>" % (self.__class__.__name__, self.id, self.name)
        elif self.id:
            return "<%s: %s>" % (self.__class__.__name__, self.id)
        return "<%s>" % self.__class__.__name__

    def get_by_slug(self, slug: str) -> bool:
        """Get a Tag by the slug."""
        return self.get_by_field("slug", slug)

    def save(self):
        """Save a Tag, updating the slug to a URL safe value."""
        self.slug = xlate.slugify(self.name)
        super(Tag, self).save()

# End File: politeauthority/bookmarky-api/src/bookmarky/api/models/tag.py
