from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt
import urllib2

#TODO, use csrf in the future.
@csrf_exempt
def locationResolver(request):
  
  if request.is_ajax():
    try:
      latitude = str(request.POST['lat'])
      longitude = str(request.POST['lon'])
      url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=" + latitude + "," + longitude + "&sensor=false"
      
      try:
	response = urllib2.urlopen(url)
	return HttpResponse(response.read())
      except:
	return HttpResponse("Error: could not resolve location!")
      
    except:
      return HttpResponse("Error: bad request!")
  else:
    raise Http404