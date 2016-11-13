#!/usr/bin/env python

import bottle
import re
import pymongo
from bson.json_util import dumps

__author__ = 'oleg'

client = pymongo.MongoClient()
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
    data = bottle.request.json # the creator must also be
    try:

        try:
            activities = 'SuggestedActivities'
            collection2 = db[('%s' % activities)]
            all_activities = []
            for i in collection2.find({'name': {'$in': data['activities']}}):
                i['downs'] = []
                i['ups'] = []
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
    obj = collection.find(data).sort({'start_date_timestamp':-1})
    return dumps(obj)


@bottle.route('/get_trips_by_person', method='POST')
def get_trips():
    collection = db['Trip']
    bottle.response.content_type = 'application/json'
    data = bottle.request.json
    obj = collection.find({'persons': {'$in': [data['email']]}}).sort('creation_timestamp', pymongo.DESCENDING)
    return dumps(obj)


@bottle.route('/create_activity', method='POST')
def create_activity():
    collection = db['SuggestedActivities']
    bottle.response.content_type = 'application/json'
    data = bottle.request.json
    data['ups'] = []
    data['downs'] = []
    obj = collection.insert_one(data)
    return dumps(obj)


@bottle.route('/get_activity', method='POST')
def get_activity():
    collection = db['SuggestedActivities']
    bottle.response.content_type = 'application/json'
    data = bottle.request.json
    obj = collection.find_one(data)
    return dumps(obj)


@bottle.route('/add_activity', method='POST')
def add_activity():
    bottle.response.content_type = 'application/json'
    data = bottle.request.json


    # obj = db['Trip'].update({'name': data['trip_name']},
    #                         {'activities': { '$addToSet': { {'name': data['name'], decision: [data['user']]}}})

    obj = db['Trip'].update({'name': data['trip_name']}, {'$addToSet': {'activities': data['name']}})

    return dumps(obj)


@bottle.route('/vote_activity', method='POST')
def vote_activity():
    bottle.response.content_type = 'application/json'
    data = bottle.request.json
    if data['ups'] == '1':
        decision = 'ups'
    else:
        decision = 'downs'

    db['Trip'].update_one({'name': data['trip_name'], 'activities': {'$elemMatch': {'name': data['name']}}},
                                   {'$set': {'activities.$.ups': [], 'activities.$.downs': []}})

    db['Trip'].update_one({'name': data['trip_name'], 'activities': {'$elemMatch': {'name': data['name']}}},
                                    {'$addToSet': {'activities.$.' + decision: data['user']}})

#> db.Trip.find({name : "york"}, {activities: {$elemMatch:{name:"Central Park"}}})

    #name = activity name

    return None


@bottle.route('/search_users', method='POST')
def search_users():
    bottle.response.content_type = 'application/json'
    data = bottle.request.json
    p = '^' + data['pattern']
    return dumps(db['Users'].find({'email': re.compile(p, re.IGNORECASE)}))


@bottle.route('/find_friends', method='POST')
def find_friends():
    bottle.response.content_type = 'application/json'
    data = bottle.request.json
    collection = db['Users']
    obj = collection.find({'email': {'$ne':data['email']}})
    return dumps(obj)


@bottle.route('/get_suggested_activities', method='POST')
def get_suggested_activities():
    collection = db['SuggestedActivities']
    bottle.response.content_type = 'application/json'
    data = bottle.request.json
    obj = collection.find({'destination': data['destination']})
    return dumps(obj)


@bottle.route('/get_trip_activities_for_date', method='POST') # sorted !
def get_suggested_activities():
    collection = db['Trip']
    bottle.response.content_type = 'application/json'
    data = bottle.request.json
    obj = collection.find({'destination': data['destination']})
    return dumps(obj)


bottle.debug(True)
bottle.run(host='131.159.192.152', port=8082)  # Start the webserver, listens
