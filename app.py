#! /usr/bin/env python2
# -*- coding:utf8 -*-
#
# app.py
#
# Copyright © 2013 Mathieu Gaborit (matael) <mathieu@matael.org>
#
#
# Distributed under WTFPL terms
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.
#

"""
Simple Etherpad-Lite ReST pad viewer.
"""

import sys
import os

from docutils.core import publish_parts

from urllib2 import urlopen

# templating
from bottle import \
        jinja2_view,\
        jinja2_template

from bottle import\
        run, \
        debug, \
        request, \
        static_file, \
        get, \
        post, \
        redirect, \
        HTTPError

# try to import settings or fallback to default
try:
    from settings import *
except ImportError:
    print("Unable to load settings.\nWill use default seetings...")
    STATIC_ROOT = "./static"
    TEMPLATE_PATH = "./templates"
    PAD_BASE = 'http://pads.haum.org/'

# homemade "template" function
def template(filename, *args, **kwargs):
    return jinja2_template(os.path.join(TEMPLATE_PATH, filename), *args, **kwargs)

# Static file view
@get('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root=STATIC_ROOT)


# home
@get('/')
def home():
    """ Homepage view """

    return template("home.html")


# view of a pad
@get('/<pad_name>')
@get('/<pad_name>/')
def view_pad(pad_name):

    # get pad text
    text = urlopen(PAD_BASE+pad_name+'/export/txt').read()

    parts = publish_parts(text, writer_name='html4css1')
    pad = parts['fragment']

    return template("pad.html", {'pad_name':pad_name, 'pad':pad})


debug(True)
run(reloader=True)
