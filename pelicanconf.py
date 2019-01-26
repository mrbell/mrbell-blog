#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

home = os.path.expanduser("~")

AUTHOR = u'Michael Bell'
SITENAME = u'Michael Bell'
SITEURL = ''
SITESUBTITLE = "Father, data scientist, gamer"

TWITTER_USERNAME = 'mryanbell'

DISQUS_SITENAME = "michaelryanbellcom"

PATH = 'content'

BOOTSTRAP_THEME = 'simplex'

THEME = os.path.join(home, "Code/pelican-themes/pelican-bootstrap3")

TIMEZONE = 'America/New_York'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

LOAD_CONTENT_CACHE = False

DEFAULT_CATEGORY = "Blog"
DISPLAY_CATEGORIES_ON_MENU = True
DISPLAY_PAGES_ON_MENU = True

# Blogroll
LINKS = ()

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/mryanbell'),
          ('GitHub', 'https://github.com/mrbell'))

DEFAULT_PAGINATION = 10

STATIC_PATHS = ['CNAME', 'images', 'pages']

PLUGIN_PATHS = [os.path.join(home, "Code/pelican-plugins")]
PLUGINS = ['render_math', 'summary', 'i18n_subsites', ]
JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n'],
}

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
