"""
    Bookmarky Api
    Utitlies - Rbac
    Rbac Utilities

"""
import logging

from bookmarky.api.utils import glow

ACL = {
    "/": {
        "GET": ["read-all"],
    },
    "/info": {
        "GET": ["read-all", "read-info"],
    },
    "/api-key": {
        "GET": ["read-all", "get-api-key"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/api-keys": {
        "GET": ["read-all", "get-api-key"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/migrations": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/option": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/options": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/perm": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/perms": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/registry": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/registries": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/role": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/roles": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/role-perm": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/role-perms": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/scan-raw": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/scan-raws": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/scan": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/scans": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["delete-all"],
    },
    "/scanner": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/scanners": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/user": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/users": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/who-am-i": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
}


def check_role_uri_access(user_role_perms: list, request) -> bool:
    """Checks a list of user role perms against the ACL list, checking to see if they line up.
    @todo: Unit test this, it's BRITTLE AF
    :unit-test: TestApiUtilsRbac::test__check_role_uri_access
    """
    rp_og = request.path
    if rp_og.count("/") > 1:
        rp = rp_og[rp_og.find("/"):rp_og.rfind("/")]
    else:
        rp = rp_og

    if rp not in ACL:
        logging.warning("Request path: %s not in ACL" % rp)
        return False
    acl_route = ACL[rp]
    rm = request.method

    if rm not in acl_route:
        logging.warning("Request method: %s not in ACL path: %s" % (rm, rp))
        return False
    acl_route_method = acl_route[rm]
    # print("has %s:" % user_role_perms)
    # print("needs %s:" % acl_route_method)

    for perm in acl_route_method:
        if perm in user_role_perms:
            return True
    return False


def get_perms_by_role_id(role_id: int) -> list:
    """Get all enabled RolePerm slug names for a given Role id."""
    sql = """
    SELECT p.name, p.slug_name
    FROM roles as r
    JOIN role_perms as rp
        ON r.id = rp.role_id
    JOIN perms as p
        ON rp.perm_id = p.id
    WHERE
        r.id = %s
        AND
        rp.enabled is True;

    """ % role_id
    glow.db["cursor"].execute(sql, (role_id,))
    res = glow.db["cursor"].fetchall()
    role_perms = []
    for rp in res:
        role_perms.append(rp[1])
    return role_perms

# End File: bookmarky/src/bookmarky/api/utils/rbac.py
