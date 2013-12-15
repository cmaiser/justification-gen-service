from TwitterSearch import *
import os
import re
import nltk

def getTweets(latitude, longitude, keywords, distance, andOr, logger, properties):
  
  returnDict = {}
  returnDict["returnMessage"] = "A server error occured in tweetAccessor.getTweets"

  try:

    if andOr == "or":
      #build keyword string
      keywordString = ""
      for i in range(len(keywords)):      
	keywordString = keywordString + keywords[i]
	if i + 1 < len(keywords):
	  keywordString = keywordString + "+OR+"

      logger.debug("tweetAccessor.getTweets - Using keywords " + keywordString)

    #create TwitterSeachOrder and set args
    tso = TwitterSearchOrder()
    if andOr == "or":
      tso.setKeywords([keywordString])
    elif andOr == "and":
      tso.setKeywords(keywords)
    tso.setLanguage('en')
    tso.setGeocode(latitude, longitude, distance, False)
    tso.setCount(100)
    tso.setIncludeEntities(False)
    
    #set TwitterSearch authentication args from properties
    ts = TwitterSearch(
      consumer_key = properties["twitter_consumer_key"],
      consumer_secret = properties["twitter_consumer_secret"],
      access_token = properties["twitter_access_token"],
      access_token_secret = properties["twitter_access_token_secret"]
    )

    logger.debug("tweetAccessor.getTweets - Searching Twitter")
    
    results = []
    ctr = 0
    
    
    tweets = ts.searchTweetsIterable(tso)
    for tweet in tweets:
      
        ctr = ctr + 1

	result = {}
	result['user'] = "@" + tweet['user']['screen_name']
	result['text'] = tweet['text']
	result['date'] = tweet['created_at']
	result['keywords'] = keywords
	
	if "geo" in tweet.keys():
	  result['geo']  = tweet['geo']
	if "location" in tweet.keys():
	  result['location'] = tweet['location']
	  
	#filter out retweets(RT)  
	isRT = re.match(r'RT', result['text'])
	
	if not isRT:
	  results.append(result)
	  
	if ctr == 100:
	  break
    
    #contains metadata from last query
    metaData = ts.getMetadata()
        
    returnDict = results
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
    
    
    