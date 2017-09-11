import json
import oauth2 as oauth
import urllib2 as urllib


class TwitterReader:

    def __init__(self):
        config = json.load("../config.json")
        self.oauth_token    = oauth.Token(key=config["access_token"], secret=config["access_token_secret"])
        self.oauth_consumer = oauth.Consumer(key=config["consumer_key"], secret=config["consumer_secret"])
        self.signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
        self.http_handler  = urllib.HTTPHandler()
        self.https_handler = urllib.HTTPSHandler()


    def request_from_twitter(self,url, http_method, parameters):
        req = oauth.Request.from_consumer_and_token(self.oauth_consumer, token=self.oauth_token,
                                                  http_method=http_method, http_url=url, parameters=parameters)

        req.sign_request(self.signature_method_hmac_sha1, self.oauth_consumer, self.oauth_token)

        if http_method == "POST":
            encoded_post_data = req.to_postdata()
        else:
            encoded_post_data = None
        url = req.to_url()

        opener = urllib.OpenerDirector()
        opener.add_handler(self.http_handler)
        opener.add_handler(self.https_handler)
        response = opener.open(url, encoded_post_data)
        return response


    def fetch_samples(self):
        url = "https://stream.twitter.com/1.1/statuses/sample.json"
        twitter = TwitterReader()
        response = twitter.request_from_twitter(url, "GET", [])
        for line in response:
            yield line.strip()


class TwitterStreamListener(tweepy.StreamListener):
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='docker:9092', value_serializer=lambda v: json.dumps(v))
        self.tweets = []

    def on_data(self, data):
        text = json.loads(data)[u'text']
        self.producer.send('iphone', text)
        self.producer.flush()
        print(text)

    def on_error(self, status_code):
        if status_code == 420:
            return False


# -*- coding: utf-8 -*-

import json
import tweepy
import socket
import sys
import time

from utils import Util
from kafka import KafkaProducer
from kafka.errors import KafkaError
from kafka.client import KafkaClient

def initialize():
    with open('../config.json') as config_data:
        config = json.load(config_data)

    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(config['access_token'], config['access_token_secret'])
    api = tweepy.API(auth)

    stream = TwitterStreamListener()
    twitter_stream = tweepy.Stream(auth = api.auth, listener=stream)
    twitter_stream.filter(track=['iphone'], async=True)





if __name__ == "__main__":
    initialize()