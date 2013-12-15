import re

def generateExcusesFromData(tweets, traffic, weather, holidays, logger):
  
  logger.debug("excuseGenerator - generateExcuses accessed")
  
  results = {}
  
  results["excuses"] = {"healthExcuse": {}, "trafficExcuse": {}, "weatherExcuse": {}, "holidayExcuse": {}}
  results["metadata"] = {}
  
  #proces health excuses
  
  masterKeywordCounter = {}
  
  results["excuses"]["healthExcuse"]["tweets"] = tweets
  
  logger.debug("Generating excuse from " + str(len(tweets)) + " Tweets.")

  #for tweet in tweets:
    #for keyword in tweet.keywords:
      #bob = ""
      #logger.debug("Keyword " + keyword + ", Text " + tweet.text)
      #matchObj = re.findall(keyword, tweet.text)
      #if keyword in masterKeywordCounter.keys():
	#masterKeywordCounter[keyword] += len(matchObj)
      #else:
	#masterKeywordCounter[keyword] = len(matchObj)

  results["excuses"]["healthExcuse"]["text"] = "This is the health related excuse."
  
  logger.debug("WTF")
  
  #process traffic excuses
  
  logger.debug("Generating excuse from " + str(len(traffic.incidents)) + " Traffic Alerts!")
  
  results["excuses"]["trafficExcuse"]["traffic"] = traffic
  results["excuses"]["trafficExcuse"]["text"] = "This is the traffic related excuse."
  
  #process weather excuses
  
  logger.debug("Generating excuse from " + str(len(weather.alerts)) + " Weather Alerts!")
  
  results["excuses"]["weatherExcuse"]["weather"] = weather
  results["excuses"]["weatherExcuse"]["text"] = "This is the weather related excuse."
  
  #process holiday excuse
  
  logger.debug("Generating excuse from " + str(len(holidays)) + " Holidays!")
  
  results["excuses"]["holidayExcuse"]["holidays"] = holidays
  
  if len(holidays) > 0:
    results["excuses"]["holidayExcuse"]["text"] = "Today is " + holidays[0] + "!"
  else:
    results["excuses"]["holidayExcuse"]["text"] = "Today isn't a holiday, and that makes me sad."
  
  return results

	
	#results
	  #excuses<dict>
	    #healthExcuse
	      #tweets<list>
	      #text
	      #keywords
	    #trafficExcuse
	      #traffic<list>
	      #text
	    #weatherExcuse
	      #weather<list>
	      #text
	    #holidayExcuse
	      #holidays<list>
	      #text
	  #metadata
	    #elapsedTime