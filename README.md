# What does this do?
This is a radicale plugin to give users access to every principal collection matching the name of a OS group they are in. Group membership is taken from grp.
The plugin simply checks if a user owns the calendar or is member of the group that owns
the calendar and gives **read** and **write** permissions if the check is successful.

The following configuration is needed:

```
[rights]

type = radicale-rights-ldap

# Optional; Strip a prefix from the OS groups.
group_prefix="loc"
```
