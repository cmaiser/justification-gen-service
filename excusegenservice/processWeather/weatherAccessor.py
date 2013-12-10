import urllib2
import json

def getWeatherAlerts(cityName, stateShortName, properties, logger):
  url = "http://api.wunderground.com/api/" + properties["weather_underground_key"] + "/alerts/q/" + stateShortName + "/" + cityName + ".json"

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