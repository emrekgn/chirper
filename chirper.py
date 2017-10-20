#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tweepy
from credentials import *


if __name__ == '__main__':
    # Credentials
    cred = Credentials();
    curr_cred = cred.next_credentials()

    # Auth Twitter API
    auth = tweepy.OAuthHandler(curr_cred['consumer_key'], curr_cred['consumer_secret'])
    auth.set_access_token(curr_cred['access_token'], curr_cred['access_token_secret'])
    api = tweepy.API(auth)

    # Place ID
    # TODO parametric geolocation
    places = api.geo_search(query="Turkey", granularity="country")
    place_id = places[0].id

    # TODO use both Search API and Streaming API
    # TODO when exception occurs, swith to another cred
    tweets = api.search(q="place:%s" % place_id)
    for tweet in tweets:
        print(tweet.text + " | " + tweet.place.name if tweet.place else "Undefined place")
