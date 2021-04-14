#!/usr/bin/python3

from os import path
from uuid import uuid4
import radicale
import sys


def create_collection(store,
                      user,
                      displayname,
                      calendar_description,
                      color="#a1bc9bff"):
    props = {
        "C:calendar-description": calendar_description,
        "C:supported-calendar-component-set": "VEVENT,VJOURNAL,VTODO",
        "D:displayname": displayname,
        "ICAL:calendar-color": color,
        "tag": "VCALENDAR",
        "is_group_calendar": "true",
    }
    uuid = str(uuid4())
    store.create_collection('/'+path.join(user, uuid), props=props)


# Create collection for every group in calendar_groups,
# if it doesn't already exists
def create_group_calendar(group, store):
    collections = store.discover('/'+group, depth=1)
    group_calendar_exists = False
    for collection in collections:
        if collection.get_meta().get("is_group_calendar", "true"):
            group_calendar_exists = True
    if not group_calendar_exists:
        create_collection(
            store,
            group,
            "{} group calendar".format(group),
            "Default group calendar of {}".format(group),
        )


def parse_sep_list(instring, sep=","):
    return list(map(str.strip, instring.split(sep)))


def main():
    config = radicale.config.load([sys.argv[1]])
    calendar_groups = parse_sep_list(sys.argv[2])
    store = radicale.storage.load(config)
    for group in calendar_groups:
        create_group_calendar(group, store)
    return 0


if __name__ == "__main__":
    main()
