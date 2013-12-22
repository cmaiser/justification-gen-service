import urllib2
import json
import os

def getTraffic(latitude, longitude, milesFromCenter, logger, properties):
  url = "http://www.mapquestapi.com/traffic/v2/incidents?key=" + properties["mapquest_key"] + "&boundingBox=" + getBoundingBox(latitude, longitude, milesFromCenter, logger) + "&filters=construction,incidents&inFormat=kvp&outFormat=json"

  logger.debug("URL for traffic: " + url)

  try:

    response = urllib2.urlopen(url)
    data = json.load(response)
    return data
  
  except urllib2.HTTPError, e:
    logger.error('trafficAccessor.getTraffic HTTPError = ' + str(e.code))
  except urllib2.URLError, e:
    logger.error('trafficAccessor.getTraffic URLError = ' + str(e.reason))
  except httplib.HTTPException, e:
    logger.error('trafficAccessor.getTraffic HTTPException')
  #finally:
  #  logger.debug('trafficAccessor.getTraffic RETURN')
  #  return data
  
def getBoundingBox(latitude, longitude, milesFromCenter, logger) :
  
  #These values are temporary until I actually do the math
  
  #close to accurate
  approxLatDegreeMiles = 69
  
  #accurate around 40 degrees north
  approxLonDegreeMiles = 53
  
  #calculate upper left
  ulLat = latitude + float(milesFromCenter) / float(approxLatDegreeMiles)
  ulLon = longitude + float(milesFromCenter) / float(approxLonDegreeMiles)
  
  #calculate lower right
  lrLat = latitude - float(milesFromCenter) / float(approxLatDegreeMiles)
  lrLon = longitude - float(milesFromCenter) / float(approxLonDegreeMiles)
  
  box = str(ulLat) + "," + str(ulLon) + "," + str(lrLat) + "," + str(lrLon)

  return box