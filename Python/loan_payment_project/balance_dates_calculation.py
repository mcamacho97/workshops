from datetime import timedelta
from datetime import datetime
from pytz import timezone

def balance_dates_calculation(payment_day1, payment_day2):
    opening_date = (datetime.now(tz = timezone("America/Managua")))
    SPP_day = opening_date.day
    payment_date = (opening_date + timedelta(days=45))
    print(f"Al cliente le pagan los {payment_day1} y {payment_day2}")
    print(f'La fecha de apertura es {opening_date}')
    print(f'La fecha maxima del SPP es {payment_date}')
    if (SPP_day > payment_day2):
        print (payment_date.replace(day=payment_day2).strftime("%Y-%m-%d"))
    else:
        print (payment_date.replace(day=payment_day1).strftime("%Y-%m-%d"))

balance_dates_calculation(15,30)