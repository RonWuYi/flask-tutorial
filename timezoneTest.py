from datetime import datetime

from pytz import timezone, utc

d = datetime(2012, 12, 21, 9, 30, 0)

print(d)

central = timezone('US/Central')
loc_d = central.localize(d)
print(loc_d)

bang_d = loc_d.astimezone(timezone ('Asia/Kolkata'))
print(bang_d)

utc_d = loc_d.astimezone(utc)

print(utc_d)