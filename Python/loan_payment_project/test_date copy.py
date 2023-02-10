from datetime import timedelta
from datetime import datetime
from pytz import timezone

#El cliente le pagan el 5 y el 20
payment_day1 = 15
payment_day2 = 30
#opening_date = (datetime.now(tz = timezone("America/Managua")))
opening_date = datetime(2022, 10, 16)
payment_date = (opening_date + timedelta(days=45))
x_plazo = 12
raw_dates = [] 
balance_dates = []
SPP_day = payment_date.day
print(SPP_day)
counter = 0

print(f"Al cliente le pagan los {payment_day1} y {payment_day2}")
print(f'La fecha de apertura es {opening_date}')
print(f'La fecha maxima del SPP es {payment_date}')

while counter <= x_plazo:
    if (SPP_day > payment_day2):
        raw_dates.append(payment_date.replace(day=payment_day2))
    else:
        raw_dates.append(payment_date.replace(day=payment_day1))
    
    payment_date = (raw_dates[counter] + timedelta(days=45))
    counter = counter + 1

for dateTest in raw_dates:
    balance_dates.append(dateTest.strftime("%Y-%m-%d"))
print(balance_dates)