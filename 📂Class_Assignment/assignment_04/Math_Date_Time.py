#The Date and Time
import time
ticks = time.time()
print("Number of ticks since 12:00am, January 1, 1970:",ticks)

#Geting the Formatted Time
import time
localtime = time.localtime(time.time())
print("Local current time:", localtime)

#Calender
import calender
cal = calender.math(2025, 1)
print("Here is a calender:")
print(cal)

from datetime import date
date1 = date(2023, 4, 19)
print("Date:", date1)
date2 = date(2023, 4, 25)
print("Date:", date2)

import datetime
x = datetime.datetime.now()
print(x)

a = datetime.datetime(2025 , 10 , 35)
print(a.strftime("%A"))
print(a.strftime("%Y"))
print(a.strftime("%f"))
print(a.strftime("%B"))