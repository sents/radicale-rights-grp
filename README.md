# What does this do?
This is a radicale plugin to give users access to every principal collection matching the name of a OS group they are in. Group membership is taken from grp.
The plugin simply checks if a user owns the calendar or is member of the group that owns
the calendar and gives **read** and **write** permissions if the check is successful.

To actually discover collections that you have read access to, but don't own, you'll need something
mirroring your readable collections in your own path.<br>
For example: <https://github.com/sents/radicale-share-collections>

The following configuration is needed:

```
[rights]

type = radicale-rights-ldap

# Optional; Strip a prefix from the OS groups.
group_prefix="loc"
```

This package also provides a command to create a canonical collection for a list of comma
separated groups with `radicale_create_groups.py /etc/radicale/config group1,group2,...`.
