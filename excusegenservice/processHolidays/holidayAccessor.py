import urllib2
import json

def getHolidays(day, month, year, logger):
  url = "http://holidayapi.com/v1/holidays?country=US&year=" + year + "&month=" + month + "&day=" + day

  try:

    response = urllib2.urlopen(url)
    data = json.load(response)
    return data
  
  except urllib2.HTTPError, e:
    logger.error('holidayAccessor.getHolidays HTTPError = ' + str(e.code))
  except urllib2.URLError, e:
    logger.error('holidayAccessor.getHolidays URLError = ' + str(e.reason))
  except httplib.HTTPException, e:
    logger.error('holidayAccessor.getHolidays HTTPException')