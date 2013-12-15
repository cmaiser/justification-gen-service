#!/usr/bin/python

import re
from django.conf import settings

def getHolidays(day, month, year, logger):
  
  holidayList = []
    
  path = settings.PROJECT_ROOT + "/config/holidays.txt"
  
  logger.debug("retrieving holidays - file path: " + path)
  
  for line in open(path):
    matchObj = re.match(r'(\d{4})\s(\d{2})\s(\d{2})\s(.+)', line)
    
    if matchObj:
      if matchObj.group(1) == year and matchObj.group(2) == month and matchObj.group(3) == day:
        holidayList.add(matchObj.group(4))

  return holidayList