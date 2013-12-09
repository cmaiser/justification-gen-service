import urllib2
import json
from django.conf import settings
import os

def getTraffic(latitude, longitude, milesFromCenter, logger):
  url = "http://www.mapquestapi.com/traffic/v2/incidents?key=" + getMapquestKey(logger) + "&boundingBox=" + getBoundingBox(latitude, longitude, milesFromCenter, logger) + "&filters=construction,incidents&inFormat=kvp&outFormat=json"

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

def getMapquestKey(logger):
      
  try:
    #get path to properties file
    path = settings.PROJECT_ROOT + "/config/mapquestapi.properties"

    logger.debug("trafficAccessor.getMapquestKey - file path: " + path)

    #read properties into properties dict
    properties = dict(line.strip().split('=') for line in open(path))

    logger.debug("trafficAccessor.getMapquestKey - Successfully read mapquestapi.properties")

  except IOError, e:
    logger.error("trafficAccessor.getMapquestKey - " + e.errno)
  except Exception, e:
    logger.error("trafficAccessor.getMapquestKey - " + e.errno)
  finally:
    return properties["key"] || "fail"