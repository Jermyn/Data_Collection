import dateutil.relativedelta
from datetime import datetime

rd = dateutil.relativedelta.relativedelta(datetime(2014, 4, 1), datetime.now())
print(rd.microseconds/1000)