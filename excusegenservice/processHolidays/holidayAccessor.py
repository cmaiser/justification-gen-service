import re
from django.conf import settings

def getHolidays(day, month, year, logger):
  
  holidayList = []
  
  if len(day) == 1:
    day = "0" + day
  
  if len(month) == 1:
    month = "0" + month
    
  path = settings.PROJECT_ROOT + "/config/holidays.txt"
  
  logger.debug("retrieving holidays - file path: " + path)
  
  for line in open(path):
    matchObj = re.match(r'(\d{4})\s(\d+)\s(\d+)\s(.+)', line)
    
    if matchObj:
      if matchObj.group(1) == year and matchObj.group(2) == month and matchObj.group(3) == day:
        holidayList.append(matchObj.group(4))

  return holidayList