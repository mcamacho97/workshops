from __future__ import print_function
# import requests
import urllib
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from datetime import datetime, timedelta
import os
import sys
import json
import logging

def testing(event, context):

    logger.info(event)
    
    timeZone = 0
    
    companyID = "BLNI"
    
    try:
        timeZone = os.environ[companyID + "_TIME_ZONE"] 
    except Exception as e:
        raise Exception("CompanyID no válido" + str(e))
    
    fecha = datetime.now() + timedelta(hours=int(timeZone))
    
    # 0 es Lunes
    weekday = fecha.weekday()
    currentHour = fecha.hour
    
    isWorkingTime = False
    
    if companyID in ["BLNI", "BLPA", "BLCR", "BLHN"] and \
        (weekday in range(0, 5) and currentHour in range(8, 17)) or \
        (weekday == 5 and currentHour in range(8, 12)):
        isWorkingTime = True
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
    
    return print(response)