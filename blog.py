#!/usr/bin/env python

from pymongo import MongoClient
import bottle
from bson.json_util import dumps

__author__ = 'oleg'

client = MongoClient()
db = client.test

# This route is the main page of the blog
@bottle.route('/')
def blog_index():
    return None


@bottle.route('/create_trip', method='POST')
def create_trip():
    bottle.response.content_type = 'application/json'
    data = dumps(bottle.request.json)
    print data
    return 'ok'


@bottle.route('/create_user', method='POST')
def create_user():
    collection = db['Users']
    bottle.response.content_type = 'application/json'
    data = bottle.request.json
    obj_id = collection.insert_one(data)
    obj = collection.find_one({'_id': obj_id.inserted_id})
    return dumps(obj)


@bottle.route('/get_user', method='POST')
def get_user():
    collection = db['Users']
    bottle.response.content_type = 'application/json'
    data = bottle.request.json
    obj = collection.find_one({'email': data['email']})
    return dumps(obj)


@bottle.route('/create_trip', method='POST')
def create_trip():
    collection = db['Trip']
    bottle.response.content_type = 'application/json'
    data = bottle.request.json

    try:
        name = data['name']
        sdate = data['sdate']
        edate = data['edate']
        source = data['source']
        dest = data['destination']
        users = data['users']
        activities = data['activities']
        obj = collection.insert_one()
    except:
        print('Error')
        return None

    return dumps(obj)


@bottle.route('/get_trip', method='POST')
def get_trip():
    collection = db['Trip']
    bottle.response.content_type = 'application/json'
    data = bottle.request.json


@bottle.route('/create_activity', method='POST')
def create_activity():
    pass


@bottle.route('/get_activity', method='POST')
def get_activity():
    pass

bottle.debug(True)
bottle.run(host='131.159.192.152', port=8082)  # Start the webserver, listens
