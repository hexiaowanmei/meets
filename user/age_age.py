import time
import datetime

def CalculateAge(Date):
    '''Calculates the age and days until next birthday from the given birth date'''
    try:
      Date = Date.split('-')
      BirthDate = datetime.date(int(Date[0]), int(Date[1]), int(Date[2]))
      Today = datetime.date.today()
      if (Today.month > BirthDate.month):
        NextYear = datetime.date(Today.year + 1, BirthDate.month, BirthDate.day)
      elif (Today.month < BirthDate.month):
        NextYear = datetime.date(Today.year, Today.month + (BirthDate.month - Today.month), BirthDate.day)
      elif (Today.month == BirthDate.month):
        if (Today.day > BirthDate.day):
          NextYear = datetime.date(Today.year + 1, BirthDate.month, BirthDate.day)
        elif (Today.day < BirthDate.day):
          NextYear = datetime.date(Today.year, BirthDate.month, Today.day + (BirthDate.day - Today.day))
        elif (Today.day == BirthDate.day):
          NextYear = 0
      Age = Today.year - BirthDate.year
      if NextYear == 0: #if today is the birthday
        return '%d, days until %d: %d' % (Age, Age+1, 0)
      else:

        return Age
    except:
      return 'Wrong date format'
