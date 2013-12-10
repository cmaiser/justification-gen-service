import urllib2
import json

def getHolidays(day, month, year, logger):
  
  url = "http://holidayapi.com/v1/holidays?country=US&year=" + year + "&month=" + month + "&day=" + day
  hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
  
  logger.debug("holidayAccessor.getHolidays - Accessing " + url)

  try:
  
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req)
    data = json.load(response)
    return data
  
  except urllib2.HTTPError, e:
    logger.error('holidayAccessor.getHolidays HTTPError = ' + str(e.code))
  except urllib2.URLError, e:
    logger.error('holidayAccessor.getHolidays URLError = ' + str(e.reason))