"""
    Bookmarky Introspect
    Debug

"""
from psycopg2 import sql

# from bookmarky.api.models.bookmark import Bookmark
from bookmarky.api.utils import glow
from bookmarky.api.utils import db
# from bookmarky.api.utils import sql_tools


db.connect()


class Debug:

    def run(self) -> list:
        # self.run_query_debug()
        self.run_param_1()

    def run_query_debug(self):
        a_list = [2, 3]
        sql = """
            SELECT *
            FROM bookmarks
            WHERE tags IN %s
        """
        the_args = tuple((a_list))
        print(sql)
        print(the_args)
        glow.db["cursor"].execute(sql, the_args)
        x = glow.db["cursor"].fetchall()
        for result in x:
            print(result)
            print("")
        # import ipdb; ipdb.set_trace()

    def run_query_2(self):
        items = [2, 3]
        sql = """
            SELECT *
            FROM bookmarks
            WHERE tags IN %s
        """
        glow.db["cursor"].execute(sql, tuple(items))
        x = glow.db["cursor"].fetchall()
        for result in x:
            print(result)
            print("")
        # import ipdb; ipdb.set_trace()

    def run_param_1(self):
        items = [2, 3]
        query = """
            SELECT *
            FROM bookmarks
            WHERE tags IN (%s, %s)
        """
        thing = (sql.Literal(items[0]), sql.Literal(items[1]))
        glow.db["cursor"].execute(query, thing)
        # x = glow.db["cursor"].fetchall()

    def run_query_hack(self):
        """This works but is gross."""
        items = [2, 3]
        sql = """
            SELECT *
            FROM bookmarks
            WHERE tags IN(%s)
        """
        query = sql.SQL("""
            SELECT *
            FROM bookmarks
            WHERE tags IN ({tag1}, {tag2})
        """).format(
            tag1=sql.Literal(items[0]),
            tag2=sql.Literal(items[1])
        )
        # formatted = ""
        # for item in items:
        #     # formatted += "{%s}," % sql_tools.sql_safe(item)
        #     formatted += "%s," % item
        # formatted = formatted[:-1]
        # print(formatted)
        # glow.db["cursor"].execute(sql, (formatted,))
        glow.db["cursor"].execute(query, (items,))
        x = glow.db["cursor"].fetchall()
        for result in x:
            print(result)
            print("")

    def run_query_ai(self):
        items = ["2", "3"]
        query = sql.SQL("SELECT id, name, tags, url FROM bookmarks WHERE tags @> ARRAY[{}]::TEXT[]").format(
            sql.SQL(',').join(map(sql.Literal, items))
        )
        query = sql.SQL("SELECT id, name, tags, url FROM bookmarks WHERE tags @> ARRAY[{}]::TEXT[]").format(
            sql.SQL(',').join(map(sql.Literal, items))
        )
        glow.db["cursor"].execute(query)
        results = glow.db["cursor"].fetchall()
        print(results)
        for result in results:
            print(result)

    def run_query(self):
        sql = """
            SELECT *
            FROM bookmarks
            WHERE tags IN('{2}', '{3}')
        """
        glow.db["cursor"].execute(sql)
        x = glow.db["cursor"].fetchall()
        for result in x:
            print(result)
            print("")


if __name__ == "__main__":
    Debug().run()


# End File: politeauthority/bookmarky/src/bookmarky/introspect/debug.py
