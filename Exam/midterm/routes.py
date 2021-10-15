from flask import Blueprint, json, render_template, request
import string
from random import choices, randint
import datetime

from flask.wrappers import Response

twitter = Blueprint('short',__name__)

users = []




@twitter.route("/")
def index():
    return "<p>Twitter API</p>"

@twitter.route('/users', methods=['POST'])
def add_users():
    req = request.get_json() 
    user_data={
        "name": req['name'],
        "email": req['email'],
        "id": randint(1,100),
        "tweets": [],
        "followers": []
    }
    users.append(user_data)
    return json.dumps(user_data)

@twitter.route('/users/<user_id>/followers/<follower_id>', methods=['PATCH'])
def update_shortlink(user_id,follower_id):
        req=request.get_json()
        print(req)
        
        for i in range(len(users)):
            if users[i].get('id')==user_id:
                currFollowers = users[i].get('followers')
                currFollowers.append(follower_id)
                users[i].update({"followers": currFollowers})          
                return json.dumps(users[i])
            
        return page_not_found()

@twitter.route('/users/<user_id>/tweets', methods=['POST'])
def add_tweets(user_id):
    req = request.get_json() 
    for i in range(len(users)):
            if users[i].get('id')==user_id:
                currTweets = users[i].get('tweets')
                new_tweet = {
                    "tweet_id": randint(1,100),
                    "tweet": req['tweet']
                }
                currTweets.append(new_tweet)
                users[i].update({"tweets": currTweets})          
                return json.dumps(new_tweet)
            
    return page_not_found()


@twitter.route('/users/<user_id>')
def get_tweets(user_id):
    for user in users:
        if user['id']== user_id:
            return json.dumps(user) 
    
    return page_not_found()

@twitter.route('/users/<user_id>/timeline')
def get_timeline(user_id):
    for user in users:
        if user['id']== user_id:
            timeline = sorted(user['tweets'], key=lambda d: d['tweet_id'])
            result = [dict(item, user_id=user_id) for item in timeline]
            return json.dumps(result) 
    
    return page_not_found()





twitter.errorhandler(404)
def page_not_found():
    response = {
    "message": "id not found",
    "description": "id not found",
    }
    return json.dumps(response), 404


