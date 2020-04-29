import grp
from radicale import rights
from radicale.storage import sanitize_path

name = "radicale-rights-grp"


class Rights(rights.BaseRights):
    def __init__(self, configuration, logger):
        super().__init__(configuration, logger)
        self.group_prefix = self.configuration.get(
            "rights", "group_prefix", fallback=None
        )

    def authorized(self, user, path, permissions):
        self.logger.debug(
            "User %r is trying to access path %r. Permissions: %r",
            user,
            path,
            permissions,
        )

        # everybody can access the root collection
        if path == "/":
            self.logger.debug("Accessing root path. Access granted.")
            return True

        user = user or ""
        sane_path = sanitize_path(path).lstrip("/")

        pathowner, _ = sane_path.split("/", maxsplit=1)
        # pathowner can be a user or a group
        if self.group_prefix:
            maybe_groupname = self.group_prefix + pathowner
        else:
            maybe_groupname = pathowner

        if user == pathowner:
            self.logger.debug("User %r is pathowner. Access granted.", user)
            return True
        else:
            try:
                group = grp.getgrnam(maybe_groupname)
                if user in group.gr_mem:
                    self.logger.debug(
                        "User %r is in pathowner group %r. Access granted.",
                        user,
                        pathowner,
                    )
                return True
            except KeyError:
                self.logger.debug(
                    "Pathowner %r is neither the user nor a valid group.", pathowner,
                )

        self.logger.debug(
            "Access to path %r is not granted to user %r.", pathowner, user
        )
        return False
