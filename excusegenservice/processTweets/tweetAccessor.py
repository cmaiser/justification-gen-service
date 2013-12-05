#!/usr/bin/python

from TwitterSearch import *

def getTweets(latitude, longitude, logger):
  
  logger.debug("tweetAccessor.getTweets - Reading in Twitter api config")
  
  properties = dict(line.strip().split('=') for line in open('excusegenservice/config/twitterapi.properties'))
  
  try:

    tso = TwitterSearchOrder()
    tso.setKeywords(['sick'])
    tso.setLanguage('en')
    tso.setGeocode(latitude, longitude, 5, False)
    tso.setCount(100)
    tso.setIncludeEntities(False)
    
    ts = TwitterSearch(
      consumer_key = properties["consumer_key"],
      consumer_secret = properties["consumer_secret"],
      access_token = properties["access_token"],
      access_token_secret = properties["access_token_secret"]
    )

    logger.debug("tweetAccessor.getTweets - Searching Twitter")
    
    results = ts.searchTweetsIterable(tso)
    
    logger.debug("tweetAccessor.getTweets - Found " + str(len(results)) + " Tweets")
    
    return results

#ctr = 0
#for tweet in ts.searchTweetsIterable(tso):
#print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )
#ctr = ctr + 1

    print "That was " + str(ctr) + " tweets." 

  except TwitterSearchException as e:
    print(e)