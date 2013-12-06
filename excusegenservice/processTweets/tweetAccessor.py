#!/usr/bin/python

from TwitterSearch import *

def getTweets(latitude, longitude, logger):
  
  logger.debug("tweetAccessor.getTweets - Reading in twitterapi.properties")
  
  try:
  
    properties = dict(line.strip().split('=') for line in open('excusegenservice/config/twitterapi.properties'))
  
    logger.debug("tweetAccessor.getTweets - Successfully read twitterapi.properties")

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
    
    results = []
    ctr = 0
    
    for tweet in ts.searchTweetsIterable(tso):

	result = {}
	result['user'] = tweet['user']['screen_name']
	result['text'] = tweet['text']
	result['date'] = tweet['created_at']
        results.append(result)

        ctr = ctr + 1

    logger.debug("tweetAccessor.getTweets - Found " + ctr + " Tweets")

    return "tweetAccessor.getTweets - Found " + ctr + " Tweets"

  except IOError, e:
    logger.error("tweetAccessor.getTweets - " + e.errno)
  except TwitterSearchException as e:
    logger.error("tweetAccessor.getTweets - " + e.errno)
  except Exception, e:
    logger.error("tweetAccessor.getTweets - " + e.errno)
