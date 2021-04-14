import grp
from radicale import rights
from radicale.pathutils import strip_path

from radicale.log import logger

name = "radicale-rights-grp"


class Rights(rights.BaseRights):
    def __init__(self, configuration):
        super().__init__(configuration)
        if "group_prefix" not in configuration.options("rights"):
            self.group_prefix = ""
        else:
            self.group_prefix = configuration.get("rights", "group_prefix")

    def authorization(self, user, path):
        logger.debug(
            "User %r is trying to access path %r.",
            user,
            path
        )

        # everybody can access the root collection
        if path == "/":
            logger.debug("Accessing root path. Access granted.")
            return "RW"

        user = user or ""
        sane_path = strip_path(path)
        full_access = "rw" if ("/" in sane_path) else "RW"
        pathowner = sane_path.split("/", maxsplit=1)[0]

        # pathowner can be a user...
        if user == pathowner:
            logger.debug("User %r is pathowner. Read & Write Access granted.", user)
            return full_access

        # ...or a group
        maybe_groupname = self.group_prefix + pathowner
        try:
            group = grp.getgrnam(maybe_groupname)
            if user in group.gr_mem:
                logger.debug(
                    "User %r is in pathowner group %r. Read & Write Access granted.",
                    user,
                    pathowner,
                )
                return full_access
        except KeyError:
            logger.debug(
                "Pathowner %r is neither the user nor a valid group.", pathowner,
            )

        logger.debug(
            "Access to path %r is not granted to user %r.", pathowner, user
        )
        return ""
