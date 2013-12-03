from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt
from processTweets.locationResolver import resolveLocation
import urllib2
import logging

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
      
      location = resolveLocation(latitude, longitude)
      
      if location["errorMsg"] == "":
	logger.debug(location["allOptions"])
	return HttpResponse(json.dumps(location))
      else:
	logger.error(location["errorMsg"])
	return HttpResponse(location["errorMsg"])

    except:
      logger.error("Bad things with the location resolver module!")
      return HttpResponse("Bad things with the location resolver module!")

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