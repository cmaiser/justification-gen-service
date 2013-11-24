from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt

#TODO, use csrf in the future.
@csrf_exempt
def locationResolver(request):
  return HttpResponse("Got it")