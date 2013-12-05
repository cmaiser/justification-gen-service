from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt
  
import urllib2
import logging
import json

from excusegenservice.processTweets.locationResolver import resolveLocation
from excusegenservice.processTweets.tweetAccessor import getTweets

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
    try:
      
      #get POST data
      latitude = str(request.POST['lat'])
      longitude = str(request.POST['lon'])

      tweets = getTweets(latitude, longitude, logger)
      
      return HttpResponse(str(len(tweets)) + " Tweets found.")
      
    except:
      
      logger.error("generateExcuses - bad request!")
      return HttpResponse("Error: bad request!")
      
  else:
    logger.error("generateExcuses - Request not ajax")
    raise Http404