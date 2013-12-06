import urllib2
import json

def resolveLocation(latitude, longitude, logger):

  logger.debug("processTweets.locationResolver.resolveLocation accessed successfully")
  url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=" + latitude + "," + longitude + "&sensor=false"
  returnList = {}
  
  try:
    
    allOptions = "\n"

    logger.debug("processTweets.locationResolver.resolveLocation attempting to connect to " + url)

    response = urllib2.urlopen(url)
    data = json.load(response)


    for component in data["results"][0]["address_components"]:
  
      if component["types"][0] != "street_number" and component["types"][0] != "route" and component["types"][0] != "neighborhood":
	allOptions += "  " + component["types"][0] +  ": " + component["long_name"] + "\n"
 
      if component["types"][0] == "locality":
	returnList["city"] = component["long_name"]
    
      if component["types"][0] == "administrative_area_level_1":
	returnList["state"] = component["long_name"]
    
      if component["types"][0] == "country":
	returnList["country"] = component["long_name"]
    

    returnList["allOptions"] = allOptions
    returnList["errorMsg"] = ""
    logger.debug('processTweets.locationResolver.resolveLocation CONNECTION SUCCESS')

  except urllib2.HTTPError, e:
    logger.error('processTweets.locationResolver.resolveLocation HTTPError = ' + str(e.code))
  except urllib2.URLError, e:
    logger.error('processTweets.locationResolver.resolveLocation URLError = ' + str(e.reason))
  except httplib.HTTPException, e:
    logger.error('processTweets.locationResolver.resolveLocation HTTPException')
  finally:
    logger.debug('processTweets.locationResolver.resolveLocation RETURN')
    return returnList