from TwitterSearch import *
from django.conf import settings
import os
import time
import re
import nltk

def getTweets(latitude, longitude, keywords, tweetLimit, distance, logger):
  
  returnDict = {}
  returnDict["returnMessage"] = "A server error occured in tweetAccessor.getTweets"

  try:

    logger.debug("tweetAccessor.getTweets - keywords: ")
    
    #get path to properties file
    path = settings.PROJECT_ROOT + "/config/twitterapi.properties"

    logger.debug("tweetAccessor.getTweets - file path: " + path)

    #read properties into properties dict
    properties = dict(line.strip().split('=') for line in open(path))

    logger.debug("tweetAccessor.getTweets - Successfully read twitterapi.properties")
    
    #build keyword string
    keywordString = ""
    for i in range(len(keywords)):      
      keywordString = keywordString + keywords[i]
      if i + 1 < len(keywords):
	keywordString = keywordString + "+OR+"

    logger.debug("tweetAccessor.getTweets - Using keywords " + keywordString)

    #create TwitterSeachOrder and set args
    tso = TwitterSearchOrder()
    tso.setKeywords([keywordString])
    tso.setLanguage('en')
    tso.setGeocode(latitude, longitude, distance, False)
    tso.setCount(100)
    tso.setIncludeEntities(False)
    
    #set TwitterSearch authentication args from properties
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
    
    #iterate through tweets until tweetLimit reached
    for tweet in ts.searchTweetsIterable(tso):

	result = {}
	result['user'] = "@" + tweet['user']['screen_name']
	result['text'] = tweet['text']
	result['date'] = tweet['created_at']
	
	if "geo" in tweet.keys():
	  result['geo']  = tweet['geo']
	if "location" in tweet.keys():
	  result['location'] = tweet['location']
	  
	#filter out retweets(RT)  
	isRT = re.match(r'RT', result['text'])
	
	if not isRT:
	  results.append(result)

        ctr = ctr + 1
        
        if ctr == tweetLimit:
	  break
	  
    #processTweets(results, keywords, logger)
        
    elapsedTime = time.time() - startTime
    
    #contains metadata from last query
    metaData = ts.getMetadata()
        
    returnDict["returnMessage"] = "Found " + str(ctr) + " tweets containing the word \"sick\" OR \"cold\" OR \"flu\" within 25 miles of your location! (Limiting results to 2 queries (200 tweets) due to <a href=\"https://dev.twitter.com/docs/rate-limiting/1.1\">Twitter rate limits</a>)<br />Elapsed time: " + str(elapsedTime) + " seconds"
    returnDict["tweets"] = results
    logger.debug("tweetAccessor.getTweets - Found " + str(ctr) + " tweets")
    logger.debug("tweetAccessor.getTweets - " + metaData["x-rate-limit-remaining"] + "/180 queries remaining this block")

  except IOError, e:
    logger.error("tweetAccessor.getTweets - " + e.errno)
  except TwitterSearchException as e:
    logger.error("tweetAccessor.getTweets - " + e.errno)
  except Exception, e:
    logger.error("tweetAccessor.getTweets - " + e.errno)
  finally:
    return returnDict

def processTweets(tweets, keywords, logger):
  
  logger.debug("tweetAccessor.processTweets accessed")
  for tweet in tweets:
    tokens = nltk.word_tokenize(tweet["text"])
    taggedTokens = nltk.pos_tag(tokens)
    
    #logger.debug(tweet["text"])
    #logger.debug(str(taggedTokens))
    
    
    