from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt
  
import urllib2
import logging
import json

logger = logging.getLogger("excusegenservice")

try:
  from excusegenservice.processTweets.locationResolver import resolveLocation
except ImportError:
  logger.error("Failed to import excusegenservice.processTweets.locationResolver import resolveLocation")
finally:
  logger.error("Successfully imported excusegenservice.processTweets.locationResolver import resolveLocation")

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
	return HttpResponse(json.dumps(location), content_type="application/json")
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
      datetime = str(request.POST['datetime'])
      location = str(request.POST['location'])
      
      returnJSON = """results: [" +
	        { \"text\" : \"Static excuse from server 1\"},
	        { \"text\" : \"Static excuse from server 2\"},
	        { \"text\" : \"Static excuse from server 3\"}
	      
	      ]"""
      return HttpResponse(returnJSON)
      
    except:
      
      logger.error("generateExcuses - bad request!")
      return HttpResponse("Error: bad request!")
      
  else:
    logger.error("generateExcuses - Request not ajax")
    raise Http404