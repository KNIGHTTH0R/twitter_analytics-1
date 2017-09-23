# -*- coding: utf-8 -*-
import tweepy
import json
import sys
import logging
from kafka import KafkaProducer

logger = logging.getLogger('twana')
logger_dir_path = "/apps/twitter_analytics/logs"
formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
logger.setLevel(logging.DEBUG)


def initialize(keywords=[], config_path='config.json'):
    try:
        with open(config_path) as config_data:
            config = json.load(config_data)
    except Exception as ex:
        logger.error("Config file is not availiable.")
        raise ex

    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(config['access_token'], config['access_token_secret'])
    api = tweepy.API(auth)

    stream = TwitterStreamListener()
    twitter_stream = tweepy.Stream(auth = api.auth, listener=stream)
    twitter_stream.filter(track=keywords, async=True)


class TwitterStreamListener(tweepy.StreamListener):
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.tweets = []

    def on_data(self, data):
        try:
            text = json.loads(data)[u'text']
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as ex:
            print(ex)
        else:
            self.producer.send('my-topic', text)
            self.producer.flush()
            print(text)

    def on_error(self, status_code):
        if status_code == 420:
            return False


if __name__ == "__main__":
    keywords = sys.argv[1:]
    initialize(keywords=keywords)
