#!/usr/bin/python3

from os import path
from grp import getgrall
from argparse import ArgumentParser
from uuid import uuid4
from re import compile as re_compile
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

def groups_from_gid_range(gidrange):
    lower, upper = map(int, gidrange.split("-"))
    return [g.gr_name for g in getgrall() if g.gr_gid in range(lower, upper + 1)]


def parse_sep_list(instring, sep=","):
    return list(map(str.strip, instring.split(sep)))

def filter_groups_with_regex(groups, regex):
    r_compiled = re_compile(regex)
    return list(filter(r_compiled.match, groups))

def strip_prefix(groups, prefix):
    return [g.lstrip(prefix) for g in groups]



def main():
    parser = ArgumentParser("Script to automatically create Radicale calendars for certain groups",
"""
Create groups from a comma separated list,
    create_group_calendars.py -g groupa,groupb config
or from a gid range
    create_group_calendars.py -i 9000-10000
The options -g and -i are mutually exclusive
Create a group matching a gid range and a regex:
    create_group_calendars.py -i 400-500 -r '^prefix_$'
""")
    parser.add_argument("config", help="path to Radicale config")
    group_args = parser.add_mutually_exclusive_group(required=True)
    group_args.add_argument("-g", "--groups",
                            help="A comma separated list of groups to create calendars for")
    group_args.add_argument("-i", "--gid-range",
                            help="A inclusive gid range (eg. '9000-9999') for which to create groups for")
    parser.add_argument("-r", "--group-name-regex",
                            help="A regex to match group names against. " +
                            "Calendars are only created for matching groups ",
                        default=".*")
    args = parser.parse_args()
    config = radicale.config.load([(args.config, False)])
    group_prefix = ("" if "group_prefix" not in config.options("rights")
                    else config.get("rights", "group_prefix"))
    calendar_groups = strip_prefix(
        filter_groups_with_regex(parse_sep_list(args.groups)
                                 if args.groups is not None
                                 else groups_from_gid_range(args.gid_range),
                                 args.group_name_regex),
        group_prefix)
    store = radicale.storage.load(config)
    for group in calendar_groups:
        create_group_calendar(group, store)
    return 0


if __name__ == "__main__":
    main()
