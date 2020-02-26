#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name="radicale-rights-grp",
    version="0.1",
    description="""
    A radicale plugin to give rights based on OS group membership """,
    long_description="""
This is a radicale plugin to give users access to every principal collection matching
    the name of a group they are in.
    """,
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    license="GNU GPLv3",
    install_requires=["radicale"],
    author="ZEDV FB-Physik FU-Berlin",
    author_email="zedv@physik.fu-berlin.de",
    url='https://gitlabph.physik.fu-berlin.de/fbedv/radicale/radicale-rights-grp',
    packages=["radicale_rights_grp"],
    entry_points={
        "console_scripts": [
            "radicale_create_groups.py = radicale_rights_ldap.create_group_calendars:main"
        ]
    },
)
