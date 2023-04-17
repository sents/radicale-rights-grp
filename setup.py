#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name="radicale-rights-grp",
    version="0.2",
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
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    license="GNU AGPLv3",
    install_requires=["radicale>=3","uuid"],
    author="Finn Krein",
    author_email="finn@krein.moe",
    url='https://github.com/sents/radicale-rights-grp',
    packages=["radicale_rights_grp"],
    entry_points={
        "console_scripts": [
            "radicale_create_groups.py = radicale_rights_grp.create_group_calendars:main"
        ]
    },
)
