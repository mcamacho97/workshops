from __future__ import print_function
# import requests
import urllib
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from datetime import datetime, timedelta, date
import os
import sys
import json
import logging
import holidays

def lambda_handler():
    #Holidays
    ni_holidays = holidays.HolidayBase() #Vacaciones Nicaragua
    ni_holidays.append({
        "2021-01-01": "Año Nuevo [New Year's Day]",
        "2021-04-01": "Jueves Santo [Maundy Thursday]",
        "2021-04-02": "Viernes Santo [Good Friday]",
        "2021-04-03": "Sábado Santo [Good Saturday]",
        "2021-05-01": "Día del Trabajo [Labour Day]",
        "2021-07-19": "Día de la Revolución [Revolution Day]",
        "2020-08-01": "Bajada de Santo Domingo",
        "2021-08-10": "Subida de Santo Domingo",
        "2021-09-14": "Batalla de San Jacinto [Battle of Saint Jacinto]",
        "2021-09-15": "Día de la Independencia [Independence Day]",
        "2021-12-08": "Concepción de María [Virgin's Day]",
        "2021-12-25": "Navidad [Christmas]"
        })
    hn_holidays = holidays.Honduras() #Vacaciones Honduras

    timeZone = 0
    
    companyID = "BLNI"
    
    try:
        timeZone = -6 
    except Exception as e:
        raise Exception("CompanyID no válido" + str(e))
    
    fecha = datetime.now() + timedelta(hours=int(timeZone))
    today = date.today()
    #fecha_holiday = today.strftime("%Y-%m-%d")
    fecha_holiday = '2021-04-03'

    # 0 es Lunes
    weekday = fecha.weekday()
    currentHour = fecha.hour
    
    isWorkingTime = False
    
    if companyID in ["BLNI", "BLPA", "BLCR", "BLHN"] and \
        (fecha_holiday not in ni_holidays) and \
        (weekday in range(0, 5) and currentHour in range(8, 17)) or \
        (weekday == 5 and currentHour in range(8, 12)):
            print(fecha_holiday)
            isWorkingTime = True
            print(isWorkingTime)
    else:
        raise Exception("CompanyID no válido")
    resultado = {
        "set_attributes": 
        {
            "isWorkingTime": isWorkingTime
        }
    }
            
    response = {
	    "statusCode": 200,
    	"headers": {
    		"Content-Type": "application/json"
    	},
    	"body": json.dumps(resultado),
    	"isBase64Encoded": False
    }
    
    return response

lambda_handler()

