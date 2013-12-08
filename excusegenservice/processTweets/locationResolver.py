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

    cityPossibilities = {}

    for component in data["results"][0]["address_components"]:
  
      if component["types"][0] != "street_number" and component["types"][0] != "route" and component["types"][0] != "neighborhood":
	allOptions += "  " + component["types"][0] +  ": " + component["long_name"] + "\n"
 
      #possibilities for city
      if component["types"][0] == "locality":
	cityPossibilities["locality"] = component["long_name"]
      if component["types"][0] == "administrative_area_level_3":
	cityPossibilities["administrative_area_level_3"] = component["long_name"]
      if component["types"][0] == "administrative_area_level_2":
	cityPossibilities["administrative_area_level_2"] = component["long_name"]
    
      #probably state
      if component["types"][0] == "administrative_area_level_1":
	returnList["state"] = component["long_name"]
    
      #probably country
      if component["types"][0] == "country":
	returnList["country"] = component["long_name"]
    
    #get city.  Order of preference: locality, administrative_area_level_3,  administrative_area_level_2
    if "locality" in cityPossibilities.keys():
      returnList["city"] = cityPossibilities["locality"]
    elif "administrative_area_level_3" in cityPossibilities.keys():
      returnList["city"] = cityPossibilities["administrative_area_level_3"]
    elif "administrative_area_level_2" in cityPossibilities.keys():
      returnList["city"] = cityPossibilities["administrative_area_level_2"]
    else:
      returnList["city"] = "Unknown City"

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