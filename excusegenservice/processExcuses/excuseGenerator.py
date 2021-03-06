import re
from random import choice

def generateExcusesFromData(tweets, traffic, weather, holidays, logger):
  
  logger.debug("excuseGenerator - generateExcuses accessed")
  
  results = {}
  
  results["excuses"] = {"healthExcuse": {}, "trafficExcuse": {}, "weatherExcuse": {}, "holidayExcuse": {}}
  results["metadata"] = {}
  
  #proces health excuses
  
  masterKeywordCounter = {}
  
  results["excuses"]["healthExcuse"]["tweets"] = tweets
  
  logger.debug("Generating excuse from " + str(len(tweets)) + " Tweets.")

  for tweet in tweets:
    for keyword in tweet["keywords"]:
      #logger.debug("Keyword " + keyword + ", Text " + tweet.text)
      matchObj = re.findall(keyword, tweet["text"])
      if keyword in masterKeywordCounter.keys():
	masterKeywordCounter[keyword] += len(matchObj)
      else:
	masterKeywordCounter[keyword] = len(matchObj)
	
  topKeywords = sorted(masterKeywordCounter, key=masterKeywordCounter.get)
  topKeywords.reverse()

  word = choice(topKeywords)

  sentence = ""
  
  logger.debug("Using keyword: " + word)
  
  if word == "sick":
    sentence += "I am very " + word + ".  "
  elif word == "flu":
    sentence += "I have the " + word + ".  "
  elif word == "cold":
    sentence += "I have a " + word + ".  "
  elif word == "disease":
    sentence += "I have a " + word + ".  "
  elif word == "fever":
    sentence += "I have a " + word + ".  "
  elif word == "virus":
    sentence += "I have a " + word + ".  "
  elif word == "vomit":
    sentence += "I need to " + word + ".  "
  else:
    sentence += "I am under the weather."


  results["excuses"]["healthExcuse"]["text"] = sentence
  results["excuses"]["healthExcuse"]["masterKeywordCounter"] = masterKeywordCounter
  
  #process traffic excuses
  
  logger.debug("Generating excuse from " + str(len(traffic["incidents"])) + " Traffic Alerts!")
  
  
  topIncident = {}
  firstIteration = True
  for incident in traffic["incidents"]:
    if firstIteration:
      topIncident = incident
      firstIteration = False
      continue
    if incident["severity"] > topIncident["severity"]:
      topIncident = incident
  
  #logger.debug("Top Incident: " + str(topIncident["severity"]) + " " + topIncident["shortDesc"])
  
  results["excuses"]["trafficExcuse"]["traffic"] = traffic
  if "shortDesc" in topIncident.keys():
    results["excuses"]["trafficExcuse"]["text"] = "I am stuck in my car.  " + topIncident["shortDesc"]
  else:
    results["excuses"]["trafficExcuse"]["text"] = "There are no traffic alerts in your area."
  
  #process weather excuses
  
  #logger.debug("Generating excuse from " + str(len(weather["alerts"])) + " Weather Alerts!")
  
  weatherExcuse = ""
  if len(weather["alerts"]) > 0:
    weatherExcuse = weather["alerts"][0]["description"]
  else:
    weatherExcuse = "It's too nice of a day!"
  
  results["excuses"]["weatherExcuse"]["weather"] = weather
  results["excuses"]["weatherExcuse"]["text"] = weatherExcuse
  
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