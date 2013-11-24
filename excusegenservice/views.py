from django.http import HttpResponse, HttpResponseRedirect, Http404

def locationResolver(request):
  return HttpResponse("Got it")