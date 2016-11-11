#!/usr/bin/env python

import pymongo
import bottle


__author__ = 'oleg'

from pymongo import connection
c = connection()

# This route is the main page of the blog
@bottle.route('/')
def blog_index():

    return {'hello':22}


bottle.debug(True)
bottle.run(host='131.159.192.152', port=8082)  # Start the webserver, listens
