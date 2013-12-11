def generateExcuses(tweets, keywords, traffic, weather, holidays, logger):
  results = {}
  
  results["excuses"] = {"healthExcuse": {}, "trafficExcuse": {}, "weatherExcuse": {}, "holidayExcuse": {}}
  results["metadata"] = {}
  
  #proces health excuses
  
  results["excuses"]["healhExcuse"]["tweets"] = tweets
  results["excuses"]["healhExcuse"]["keywords"] = keywords
  results["excuses"]["healhExcuse"]["text"] = "This is the health related excuse."
  
  #process traffic excuses
  
  results["excuses"]["trafficExcuse"]["traffic"] = traffic
  results["excuses"]["trafficExcuse"]["text"] = "This is the traffic related excuse."
  
  #process weather excuses
  
  results["excuses"]["weatherExcuse"]["weather"] = weather
  results["excuses"]["weatherExcuse"]["text"] = "This is the weather related excuse."
  
  #process holiday excuse
  
  results["excuses"]["holidyExcuse"]["holidays"] = holidays
  results["excuses"]["holidayExcuse"]["text"] = "This is the holiday related excuse."
  
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