#!/usr/bin/python

import urllib2
import json

def resolveLocation(latitude, longitude):

  url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=%f,%f&sensor=false" % (latitude, longitude)
  returnList = {}
  
  try:
    
    allOptions = ""

    response = urllib2.urlopen(url)
    data = json.load(response)

    for component in data["results"][0]["address_components"]:
  
      if component["types"][0] != "street_number" and component["types"][0] != "route" and component["types"][0] != "neighborhood":
	allOptions += "  " + component["types"][0] +  ": " + component["long_name"] + "\n"
 
      if component["types"][0] == "administrative_area_level_2":
	returnList["city"] = component["long_name"]
    
      if component["types"][0] == "administrative_area_level_1":
	returnList["state"] = component["long_name"]
    
      if component["types"][0] == "country":
	returnList["country"] = component["long_name"]
    

    returnList["allOptions"] = allOptions
    returnList["errorMsg"] = ""

  except:
    returnList["errorMsg"] = "Could not retrieve location information"
    
  finally:
    return returnList