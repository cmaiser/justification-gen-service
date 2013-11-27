from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt
import urllib2
import logging

logger = logging.getLogger("excusegenservice")

#TODO, use csrf in the future.
@csrf_exempt
def locationResolver(request):
  
  #check request for HTTP_X_REQEUSTED_WITH header
  if request.is_ajax():
    
    try:
      
      #get POST data
      latitude = str(request.POST['lat'])
      longitude = str(request.POST['lon'])
      
      logger.debug("locationResolver - POST - " + latitude + ", " + longitude)
      
      #build request URL
      url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=" + latitude + "," + longitude + "&sensor=false"
      
      try:
	
	#make request and return response text if successful
	response = urllib2.urlopen(url)
	return HttpResponse(response.read())
      
      except:
	
	logger.error("locationResolver - could not contact Google!")
	return HttpResponse("Error: could not contact Google!")
      
    except:
      
      logger.error("locationResolver - bad request!")
      return HttpResponse("Error: bad request!")
    
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