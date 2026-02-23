import datetime
# exercise 1 ----------------------------------------------------------------
today = datetime.date.today()
five_days_ago = datetime.date.fromordinal(today.toordinal() - 5)

print("Today:", today)
print("Five days ago:", five_days_ago)

# exercise 2 ----------------------------------------------------------------
today = datetime.date.today()
yesterday= datetime.date.fromordinal(today.toordinal() - 1)
tomorrow = datetime.date.fromordinal(today.toordinal() + 1)
print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)
# exercise 3 ----------------------------------------------------------------
import datetime

x = datetime.datetime.now()
print(x.strftime("%x %X"))
# exercise 4 ----------------------------------------------------------------

d1 = datetime.date.fromisoformat(input("Enter first date (YYYY-MM-DD): "))
d2 = datetime.date.fromisoformat(input("Enter second date (YYYY-MM-DD): "))

days = abs(d2.toordinal() - d1.toordinal())
seconds = days * 24 * 60 * 60

print("Difference in seconds:", seconds)