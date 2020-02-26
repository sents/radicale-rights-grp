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

    def user_in_group(self, user, group):
        if self.group_prefix is not None:
            group = self.group_prefix + group
        if user in grp.getgrnam(group).gr_mem:
            return True
        else:
            return False

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
        sane_path = sanitize_path(path)
        sane_path = sane_path.lstrip("/")
        pathowner, subpath = sane_path.split("/", maxsplit=1)
        if user == pathowner:
            self.logger.debug("User %r is pathowner. Access granted.", user)
            return True
        else:
            # Check if pathowner is group of user
            in_group = self.user_in_group(user, pathowner)
            if in_group:
                self.logger.debug(
                    "User %r is in pathowner group %r. Access granted.", user, pathowner
                )
            else:
                self.logger.debug(
                    "Access to path %r is not granted to user %r.", pathowner, user
                )
            return in_group
