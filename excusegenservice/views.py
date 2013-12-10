from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
  
import urllib2
import logging
import json
import re
import time

from excusegenservice.processTweets.locationResolver import resolveLocation
from excusegenservice.processTweets.tweetAccessor import getTweets
from excusegenservice.processTweets.tweetAccessor import processTweets
from excusegenservice.processTraffic.trafficAccessor import getTraffic
from excusegenservice.processWeather.weatherAccessor import getWeatherAlerts

logger = logging.getLogger("excusegenservice")

#TODO, use csrf in the future.
@csrf_exempt
def locationResolver(request):
  
  #check request for HTTP_X_REQEUSTED_WITH header
  if request.is_ajax():
    
    latitude = 0
    longitude = 0
    
    try:
      
      #get POST data
      latitude = str(request.POST['lat'])
      longitude = str(request.POST['lon'])
      
      logger.debug("locationResolver - POST - " + latitude + ", " + longitude)
      
    except:
      
      logger.error("locationResolver - bad request!")
      return HttpResponse("Error: bad request!")
      
    try:
      
      logger.debug("locationResolver - attempting to use locationResolver module: "  + latitude + ", " + longitude)
      
      location = resolveLocation(latitude, longitude, logger)
      
      if location["errorMsg"] == "":
	logger.debug(location["allOptions"])
	del location["allOptions"]
	return HttpResponse(json.dumps(location))
      else:
	logger.error(location["errorMsg"])
	return HttpResponse(location["errorMsg"])

    except(TypeError, ValueError) as err:
      logger.error("Server error: " + err)
      return HttpResponse("Server error: " + err)

  else:
    
    logger.error("locationResolver - Request not ajax")
    raise Http404

@csrf_exempt
def generateExcuses(request):
  if request.is_ajax():
    
    results = {}
    
    try:
      
      #get POST data
      latitude = float(request.POST['lat'])
      longitude = float(request.POST['lon'])
      cityName = str(request.POST['cityName'])
      stateShortName = str(request.POST['stateShortName'])
      
      properties = getProperties()

      startTime = time.time()

      keywords = ["sick", "cold", "flu"]
      results["tweetResults"] = getTweets(latitude, longitude, keywords, 500, 25, logger, properties)
      results["trafficResults"] = getTraffic(latitude, longitude, 25, logger, properties)
      results["weatherAlerts"] = getWeatherAlerts(cityName, stateShortName, properties, logger)
      
      elapsedTime = time.time() - startTime
      
      results["elapsedTime"] = 'Time Elapsed: %.2f seconds' % elapsedTime
      
      return HttpResponse(json.dumps(results))

    except Exception, e:
      logger.error("views.generateExcuses - GENERAL EXCEPTION")
      return HttpResponse("Error: bad request!")
      
  else:
    logger.error("generateExcuses - Request not ajax")
    raise Http404

#function to read in properties file
#for api authentication
def getProperties():
      
  #get path to properties file
  path = settings.PROJECT_ROOT + "/config/authentication.properties"
  
  logger.debug("views.getProperties - file path: " + path)

  #read properties into properties dict
  properties = dict(line.strip().split('=') for line in open(path))

  logger.debug("views.getProperties - Successfully read authentication.properties")
    
  return properties