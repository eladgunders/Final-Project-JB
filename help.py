from datetime import datetime

d1 = datetime(2021, 1, 1)
print(d1)
d2 = datetime.now()
print(d2)
print(d1.year == d2.year)