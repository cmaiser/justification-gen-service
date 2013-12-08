#!/usr/bin/python

from TwitterSearch import *
from django.conf import settings
import os
import time

def getTweets(latitude, longitude, logger):
  
  returnDict = {}
  returnDict["returnMessage"] = "A server error occured in tweetAccessor.getTweets"

  try:

    logger.debug("tweetAccessor.getTweets - keywords: ")

    path = settings.PROJECT_ROOT + "/config/twitterapi.properties"

    logger.debug("tweetAccessor.getTweets - file path: " + path)

    properties = dict(line.strip().split('=') for line in open(path))

    logger.debug("tweetAccessor.getTweets - Successfully read twitterapi.properties")

    tso = TwitterSearchOrder()
    tso.setKeywords(['sick+OR+flu+OR+cold'])
    tso.setLanguage('en')
    tso.setGeocode(latitude, longitude, 25, False)
    tso.setCount(100)
    tso.setIncludeEntities(False)
    
    ts = TwitterSearch(
      consumer_key = properties["consumer_key"],
      consumer_secret = properties["consumer_secret"],
      access_token = properties["access_token"],
      access_token_secret = properties["access_token_secret"]
    )

    logger.debug("tweetAccessor.getTweets - Searching Twitter")
    
    startTime = time.time()
    results = []
    ctr = 0
    
    for tweet in ts.searchTweetsIterable(tso):

	result = {}
	result['user'] = tweet['user']['screen_name']
	result['text'] = tweet['text']
	result['date'] = tweet['created_at']
        results.append(result)

        ctr = ctr + 1
        
        if ctr == 200:
	  break
        
    elapsedTime = time.time() - startTime
        
    returnDict["returnMessage"] = "Found " + str(ctr) + " tweets containing the word \"sick\" OR \"cold\" OR \"flu\" within 25 miles of your location! (Limiting results to 2 queries (200 tweets) due to <a href=\"https://dev.twitter.com/docs/rate-limiting/1.1\">Twitter rate limits</a>)<br />Elapsed time: " + str(elapsedTime) + " seconds"
    returnDict["tweets"] = results
    logger.debug("tweetAccessor.getTweets - Found " + str(ctr) + " tweets")

  except IOError, e:
    logger.error("tweetAccessor.getTweets - " + e.errno)
  except TwitterSearchException as e:
    logger.error("tweetAccessor.getTweets - " + e.errno)
  except Exception, e:
    logger.error("tweetAccessor.getTweets - " + e.errno)
  finally:
    return returnDict
