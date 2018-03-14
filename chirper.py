#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import jsonpickle
import tweepy
from credentials import *

# TODO argparse
country = "Turkey"
max_tweets = 1000000
tweets_per_query = 100
filename = 'tweets'
include_fields = ["text", "lang", "created_at"]


class Chirper():
    def __init__(self):
        self.cred = Credentials();
        self.twitter_api = None
        self.search_query = None
        self.tweet_count = 0

    def auth(self):
        """
        Auth Twitter API
        :return:
        """
        curr_cred = self.cred.next_credentials()
        auth = tweepy.OAuthHandler(curr_cred['consumer_key'], curr_cred['consumer_secret'])
        auth.set_access_token(curr_cred['access_token'], curr_cred['access_token_secret'])
        self.twitter_api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        if not self.twitter_api:
            print("Problem connecting to API.")
            sys.exit()

    def build_search_query(self):
        """
        Build country-specific search query
        :return:
        """
        places = self.twitter_api.geo_search(query=country, granularity="country")
        place_id = places[0].id
        self.search_query = "place:{0}".format(place_id)
        print("{0} ID is: {1}".format(country, place_id))

    def chirp(self):
        """
        Download country-specific tweets.
        
        If any exceptions occur, try to download with different credentials.
        If download rate limit exceeded, wait until it passes.
        :return:
        """
        self.auth()
        self.build_search_query()
        # Wrap json output to make it valid!
        with open("{0}.json".format(filename), 'a+') as j:
            j.write('{\n"tweets":[\n')
        while self.tweet_count < max_tweets:
            try:
                with open("{0}.json".format(filename), 'a+') as j, open("{0}.csv".format(filename), 'a+') as c:
                    for tweet in tweepy.Cursor(self.twitter_api.search, q=self.search_query).items(max_tweets):
                        if tweet.place is not None:
                            json = dict()
                            for key in include_fields:
                                if key in tweet._json:
                                    json[key] = tweet._json[key]
                            print(str(jsonpickle.encode(json, unpicklable=False)))
                            j.write(jsonpickle.encode(json, unpicklable=False) + ',\n')
                            c.write((",".join(json.values())) + '\n')
                            self.tweet_count += 1
                        if self.tweet_count % 1000:
                            print("Downloaded {0} tweets so far...".format(self.tweet_count))
            except Exception as e:
                print("Exception: {0}".format(str(e)))
                # Auth with different credentials so that we can try to continue downloading!
                self.auth()
            print("Downloaded {0} tweets! Saved to {1}".format(self.tweet_count, filename))
        # End wrapper.
        with open("{0}.json".format(filename), 'a+') as j:
            j.write('{}\n]\n}')


if __name__ == '__main__':
    chirper = Chirper()
    chirper.chirp()
