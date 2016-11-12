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
    cursor = collection.find_one({'email': data['email']})
    if cursor is None:
        obj_id = collection.insert_one({'email': data['email']})
        cursor = collection.find_one({'_id': obj_id.inserted_id})
    return dumps(cursor)


@bottle.route('/create_trip', method='POST')
def create_trip():
    collection = db['Trip']
    bottle.response.content_type = 'application/json'
    data = bottle.request.json
    try:

        try:
            collection2 = db['SuggestedActivities']
            all_activities = []
            for i in collection2.find({'name': {'$in': data['activities']}}):
                all_activities.append(i)

            data["activities"] = all_activities
        except:
            pass
        collection.insert_one(data)
    except:
        pass
    obj = collection.find_one({'name': data['name']})

    return dumps(obj)


@bottle.route('/get_trips', method='POST')
def get_trips():
    collection = db['Trip']
    bottle.response.content_type = 'application/json'
    data = bottle.request.json
    obj = collection.find(data)
    return dumps(obj)


@bottle.route('/get_trips_by_persons', method='POST')
def get_trips():
    collection = db['Trip']
    bottle.response.content_type = 'application/json'
    data = bottle.request.json
    obj = collection.find({'persons': {'$in': [data['email']]}}) #fara paranteze
    return dumps(obj)


@bottle.route('/create_activity', method='POST')
def create_activity():
    collection = db['Activity']
    bottle.response.content_type = 'application/json'
    data = bottle.request.json
    obj = collection.insert_one(data)
    return dumps(obj)


@bottle.route('/get_activity', method='POST')
def get_activity():
    collection = db['Activity']
    bottle.response.content_type = 'application/json'
    data = bottle.request.json
    obj = collection.find_one(data)
    return dumps(obj)


@bottle.route('/update_activity', method='POST')
def update_up():
    collection = db['Trip']
    bottle.response.content_type = 'application/json'
    data = bottle.request.json
    obj = collection.find_one({'name' : data['name'], 'ups': {'$exists': True}})

   # db.Trip.update({name: "Hollywood"}, {$push:{"activities": {"name": "shooting", "ups": ["oleska"]}}})


    if obj is not None: # if it has ups/downs update it, else
        db['Trip'].update({'name': data['trip_name']}, {'$push':{'activities': { 'name': data['name'], 'ups': [data['user']]}}})
    else:
        pass

    return dumps(obj)


@bottle.route('/get_suggested_activities', method='POST')
def get_suggested_activities():
    collection = db['SuggestedActivities']
    bottle.response.content_type = 'application/json'
    data = bottle.request.json
    obj = collection.find({'destination': data['destination']})
    return dumps(obj)


@bottle.route('/link_suggested_activities', method='POST')
def link_suggested_activities():
    collection = db['Trip']
    bottle.response.content_type = 'application/json'
    data = bottle.request.json
    obj = collection.find({'destination': data['destination']})
    return dumps(obj)




bottle.debug(True)
bottle.run(host='131.159.192.152', port=8082)  # Start the webserver, listens
