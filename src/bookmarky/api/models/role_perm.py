"""
    Cver Api
    Model
    RolePerm

"""
import logging

from bookmarky.shared.models.role_perm import FIELD_MAP
# from bookmarky.api.utils import sql_tools
from bookmarky.api.models.base import Base


class RolePerm(Base):

    model_name = "role_perm"

    def __init__(self, conn=None, cursor=None):
        """Create the Perm instance.
        :unit-test: TestApiModelRolePerm::test____init__
        """
        super(RolePerm, self).__init__(conn, cursor)
        self.table_name = "role_perms"
        self.field_map = FIELD_MAP
        self.createable = True
        self.setup()

    def __repr__(self):
        """Create the Perm instance.
        :unit-test: TestApiModelRolePerm::test____repr__
        """
        if self.id:
            return "<RolePerm %s:(Role.ID %s, Perm.ID %s)>" % (self.id, self.role_id, self.perm_id)
        else:
            return "<RolePerm>"

    def get_by_role_perm(self, role_id: int, perm_id: int) -> bool:
        """Create the Perm instance.
        :unit-test: TestApiModelRolePerm::test____init__
        """
        # sql = """
        #     SELECT *
        #     FROM role_perms
        #     WHERE
        #         role_id = %s AND
        #         perm_id = %s AND
        #         enabled is True
        #     LIMIT 1; """ % (sql_tools.sql_safe(role_id), sql_tools.sql_safe(perm_id))

        # @ todo verify this change works
        logging.waring("get_by_role_perm ")
        sql = """
            SELECT *
            FROM role_perms
            WHERE
                role_id = %s AND
                perm_id = %s AND
                enabled is True
            LIMIT 1; """
        self.cursor.execute(sql, (role_id, perm_id,))
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

# End File: cver/src/api/models/role_perm.py
