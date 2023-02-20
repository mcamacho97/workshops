import csv  
import json  
import io
import logging
import base64
import dateutil.parser
from datetime import datetime, timedelta
# from geolite2 import geolite2
import geoip2.database
import awswrangler as wr
import os
import ipaddress

os.environ['AWS_DEFAULT_REGION'] = "us-east-1"

from user_agents import parse
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# reader = geolite2.reader()
s3 = boto3.resource('s3')
events = boto3.client('events')
dynamodb = boto3.resource('dynamodb')

scoreboard = dynamodb.Table('Scoreboard_Usuarios_Bancanet')
                    wr.dynamodb.put_items(
                        items=[user],
                        table_name='Scoreboard_Usuarios_Bancanet'
                    )


obj = s3.Object("lafise-general-configurations-desa", "reference-data/bancanet/CustomersVIP.csv").get()['Body'].read().decode('utf-8').splitlines()

# para pruebas con usuario lafise_test


def rule_devices(device, devices):
    # para pruebas en https://developers.whatismybrowser.com/useragents/parse/748207chrome-android-sm-g9650-blink
    
    # device = "Mozilla/5.0 (Linux; Android 10; SAMSUNG SM-G9650) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/15.0 Chrome/90.0.4430.210 Mobile Safari/537.36"
    # device = "Mozilla/5.0 (Linux; Android 8.0.0; SM-G9650 Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36"
    # device = "Mozilla/5.0 (Linux; Android 10; SM-G9650 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/91.0.4472.120 Mobile Safari/537.36"
    # device = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1"
    # device = "Mozilla/5.0 (Linux; Android 10; SM-G9650 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/97.0.4692 Mobile Safari/537.36"
    # device = "Mozilla/5.0 (Linux; Android 9; SM-G9650 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/97.0.4692 Mobile Safari/537.36"
    # device = "Mozilla/5.0 (Linux; Android 9; SM-G9650 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.4692 Mobile Safari/537.36"
    # device = "Mozilla/5.0 (Linux; Roku 9; SM-G9650 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.4692 Mobile Safari/537.36"
    
    agent_string = str(device).strip()
    agent = parse(agent_string)
                
    # calculo sin versiones
    # al final dejamos la version, porque el atacante puede usar una version distinta a la habitual
    agent_light = str(agent)
    
    result = ""
    
    
    # si no detecta la funcion agente, no podemos efectuar calculos
    if agent_light == '':
        result = "No Identificado"
    else:
        # la familia es la marca del celular
        # device_family = agent.device.family
        # el device family a veces no funciona para ciertos dispositivos y devuelve other, en este caso se le hace un split mejor al string del agent
        device_family = agent_light.split(" / ")[0].strip()
        # os, es el sistema operativo
        os = agent.os.family.strip()
        os_version = agent_light.split(" / ")[1].strip() 
        
        browser = agent.browser.family.strip()
        browser_version = agent_light.split(" / ")[2].strip() 
        
        
        # buscamos dispositivos que sean el mismo, no importando la version, puede obtener varias registros de versiones del mismo dispositivo
        same_devices = [term_dict for term_dict in devices if term_dict["user_agent"].split(" / ")[0].strip() == device_family] 
        
        # si no encontramos es un dispositivo nuevo
        if len(same_devices) == 0:
            result = "Nuevo"
        else:
            # si encontramos, revisamos la version del sistema operativo si ya tiene la misma version
            if os_version in [term_dict["user_agent"].split(" / ")[1].strip() for term_dict in same_devices]:
                # si encontramos, revisamos la version del navegador si ya tiene la misma version
                if browser_version in [term_dict["user_agent"].split(" / ")[2].strip() for term_dict in same_devices]:
                    # tiene mismo dispositivo, os y version, que lo mismo es comparar con light version, pero se hace aca para respetar el flujo propuesto
                    result = "Existente"                  
                elif browser in [' '.join(term_dict["user_agent"].split(" / ")[2].strip().split(" ")[:-1]).strip() for term_dict in same_devices]:
                    # si es el mismo navegador, y no es la misma version del navegador, lo considaramos como actualizacion del browser
                    result = "Actualizado"
                else:
                    # si no encontramos ni el browser ni version de browser igual, consideramos dispositivo nuevo
                    result = "Nuevo"
            elif os in [term_dict["user_agent"].split(" / ")[1].strip().split(" ")[0].strip() for term_dict in same_devices]:
                # en este caso es mimso sistema operativo, pero version diferente               
                if browser_version in [term_dict["user_agent"].split(" / ")[2].strip() for term_dict in same_devices]:
                    # si tiene la misma version de su navegador, es considerado actualizacion de sistama operativo con mismo navegador
                    result = "Actualizado"
                elif browser in [' '.join(term_dict["user_agent"].split(" / ")[2].strip().split(" ")[:-1]).strip() for term_dict in same_devices]:
                    # en este caso, cambia de sistema operativo, mantiene su navegador, pero esta actualizado el navegador
                    result = "Actualizado"
                else:
                    # aque es que cambio de version de sistema operativo, y tiene navegador distinto
                    result = "Nuevo"
            else:
                # qqui quiere decir que encuentra un dispositivo existente, pero su sistema operativo es distinto con version distinta
                result = "Nuevo"
    return result
    
def rule_countries(country, countries): 
    result = ""
    
    # pais no identificado cuando la libreria de IPs no detecta ubicaciones
    if country == 'Unidentified':
        result = "No Identificado"
    elif country == 'Local':
        result = "Local"
    elif country not in [term_dict["pais"] for term_dict in countries]:
        result = "Nuevo"
    else:
        result = "Existente"
                    
    return result
    
                   

def lambda_handler(event, context):
    output = []
    rt_integrations = []


    # with geoip2.database.Reader('_maxminddb_geolite2/GeoLite2-City.mmdb') as reader:
    #     response = reader.city('186.32.185.50')
    #     print(response)

    # # This creates a Reader object. You should use the same object
    # # across multiple requests as creation of it is expensive.
    # with geoip2.database.Reader('/_maxminddb_geolite2/GeoLite2-City.mmdb') as reader:

    #     # Replace "city" with the method corresponding to the database
    #     # that you are using, e.g., "country".
    #     response = reader.city('190.61.80.218')
    
    
    for record in event['records']:
        # print(record['recordId'])
        payload = base64.b64decode(record['data']).decode('utf-8')
        the_json = json.loads(payload)
        
        ip_addr = the_json["AuditUserIpAddress"]

        geo_loc = None

        #ip_addr = '10.11.1.1'
        #ipaddress.ip_address(ip_addr).is_private

        if len(ip_addr) >= 8: 
            if ipaddress.ip_address(ip_addr).is_private:
                geoip_city = 'Local'
                geoip_country = 'Local'
                geoip_lat = float("12.11563611")
                geoip_lon = float("-86.2565")
                iso_code = ''
            else:
                try:
                    with geoip2.database.Reader(os.path.dirname(__file__) + '/GeoLite2-City.mmdb') as reader:
                        geo_loc = reader.city(ip_addr)
                        print(geo_loc)
                    
                    geoip_city = geo_loc.city.name
                    if geoip_city == None:
                        geoip_city = 'Unidentified'
                except Exception as e:
                    geoip_city = 'Unidentified'
                      
                try:
                    geoip_country = geo_loc.country.name
                    if geoip_country == None:
                        geoip_country = 'Unidentified'
                        
                except:
                    geoip_country = 'Unidentified'
                try:
                    geoip_lat = geo_loc.location.latitude
                    geoip_lon = geo_loc.location.longitude
    
                    if geoip_lat is None:
                        geoip_lat = float("12.11563611")
                    if geoip_lon is None:
                        geoip_lon = float("-86.2565")
                except:
                    geoip_lat = float("12.11563611")
                    geoip_lon = float("-86.2565")
                
                try:
                    iso_code = geo_loc.country.iso_code
                except:
                    iso_code = ''
        else:
            geoip_city = 'Unidentified'
            geoip_country = 'Unidentified'
            geoip_lat = float("12.11563611")
            geoip_lon = float("-86.2565")
            iso_code = ''
        
        # utcDate = datetime.strptime(the_json["AuditDatetime"], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(hours=int(+6))
        # the_json["@timestamp"] = utcDate.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        # the_json["AuditDatetime"] = utcDate.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        
        the_json["ip_iso_code"] = iso_code
        the_json["ip_country"] = geoip_country
        the_json["ip_city"] = geoip_city
        the_json["location"] = {
            "lat" : geoip_lat,
            "lon" : geoip_lon
        }
        
        company = the_json["sink_company"]
        iso_country = company[-2:]
        if iso_country == "RG":
            iso_country = "US"
            
        the_json['iso_country'] = iso_country
        if iso_country == "NI":
            country = "Nicaragua"
        elif iso_country == "HN":
            country = "Honduras"
        elif iso_country == "PA":
            country = "Panamá"
        elif iso_country == "CR":
            country = "Costa Rica"
        elif iso_country == "DO":
            country = "República Dominicana"
        else:
            country = "Estados Unidos"
        
        the_json['country'] = country
        the_json['company'] = company        
                
        # datetime.strptime(theJson["AuditDatetime"],"%Y-%m-%d %H:%M:%S.%f").isoformat()
        # jsonData[2] = datetime.strptime(jsonData[2],'%Y-%m-%d %H:%M:%S.%f').isoformat()
        try:
            the_json['UserVIP'] = str(the_json["UserName"] in [i.split(',', 1)[0].replace("\"","") for i in obj[1:]])
        except:
            the_json['UserVIP'] = "False"
        json_output = json.dumps(the_json) + "\n"
        
        try:
            # Bloque de codigo para integraciones de logons alerts
            
            nombre_usuario = str(the_json["UserName"]).lower().strip()
            
            
            # para no afectar procesamient, integraciones dentro de un try
            if (nombre_usuario != "none" and the_json["ServiceOperationName"] == 'LogOnCustom'):
                browser_user_agent = str(the_json["BrowserUserAgent"]).strip()

                # nombre_usuario = "lafise_test"
                #PRO
                #scoreboard = dynamodb.Table('Scoreboard_Usuarios_Bancanet_dev')


                usuario = scoreboard.get_item(
                    Key={
                        'usuario' : nombre_usuario
                    }
                )
                the_json_logons = the_json.copy()
                
                
                # Extraemos datos actuales del usuario, y sus dispositivos y paises
                
                the_json_logons["UserName"] = nombre_usuario
                
                fecha_ejecucion = the_json_logons["timestamp"]
                
                
                if "Item" in usuario:
                    user = usuario["Item"]
                    info_pais = ""
                    info_dispositivo = ""
                    hits = 0
                    
                    
                    # Codigo temporal para fix de timestamps de los formatos de fechas que no lo tienen
                    for i in range(len(user["paises"])):
                        if "T" not in user["paises"][i]["ultimo_login"]:
                            user["paises"][i]["ultimo_login"] = datetime.strptime(user["paises"][i]["ultimo_login"], '%Y-%m-%d %H:%M:%S.%f').isoformat()
                    
                    for i in range(len(user["dispositivos"])):
                        if "T" not in user["dispositivos"][i]["ultimo_login"]:
                            user["dispositivos"][i]["ultimo_login"] = datetime.strptime(user["dispositivos"][i]["ultimo_login"], '%Y-%m-%d %H:%M:%S.%f').isoformat()
                    
                    
                    
                    the_json_logons["alerta.paislogon.existentes"] = user["paises"]
                    the_json_logons["alerta.dispositivo.existentes"] = user["dispositivos"]
                    
                    
                    dispositivo_string = str(the_json_logons["BrowserUserAgent"]).strip()
                    dispositivo_agente = parse(dispositivo_string)
                    dispositivo_light = str(dispositivo_agente)
                    
                    resultado_dispositivo = rule_devices(the_json_logons["BrowserUserAgent"], user['dispositivos'])
                    resultado_pais = rule_countries(geoip_country, user['paises'])
                    resultado_alerta = ""
                    
                    if resultado_pais == "Local":
                        resultado_alerta = "Verde"
                    elif resultado_pais == "Existente" and (resultado_dispositivo == "Existente" or resultado_dispositivo == "Actualizado"):
                        resultado_alerta = "Verde"
                    elif resultado_pais == "Existente" and resultado_dispositivo == "Nuevo":     
                        resultado_alerta = "Amarillo"
                    elif resultado_pais == "Nuevo" and (resultado_dispositivo == "Existente" or resultado_dispositivo == "Actualizado"):
                        resultado_alerta = "Amarillo"
                    elif resultado_pais == "Nuevo" and resultado_dispositivo == "Nuevo":     
                        resultado_alerta = "Rojo"
                    else:
                        resultado_alerta = "Amarillo"
                    
                    the_json_logons["alerta.dispositivo.resultado"] = resultado_dispositivo
                    the_json_logons["alerta.paislogon.resultado"] = resultado_pais
                    the_json_logons["alerta.color"] = resultado_alerta
                    

                    
                    #calculamos el ultimo login por dispositivo o pais
                    elemento = {
                        "user_agent" : dispositivo_light,
                        "ultimo_login" : fecha_ejecucion
                    }
                    pais = {
                        "pais" : geoip_country,
                        "ultimo_login" : fecha_ejecucion
                    }
                    
                    #eliminamos el existente, y reinsertamos el nuevo calculado, simulando un upsert,
                    #el existente lo borra y recrea, al nuevo, como no lo encuentra, lo crea
                    
                    if dispositivo_light != "":
                        user["dispositivos"] = [term_dict for term_dict in user['dispositivos'] if dispositivo_light not in term_dict['user_agent']]
                        user["dispositivos"].append(elemento)
                    
                    if geoip_country != "Unidentified":
                        user["paises"] = [term_dict for term_dict in user['paises'] if geoip_country not in term_dict['pais']]
                        user["paises"].append(pais)
                    
                    
                    
                
                    the_json_logons["alerta.paislogon.paisdelogon"] = geoip_country
                    the_json_logons["alerta.dispositivo.dispositivologon"] = dispositivo_light
                    
                        
                    user["ultimo_login"] = fecha_ejecucion
                    
                    if resultado_pais == "Local":
                        the_json_logons["alerta.descripcion"] = 'Login desde Red Banco LAFISE'
                    else:
                        the_json_logons["alerta.descripcion"] = f'Dispositivo {resultado_dispositivo} y Pais {resultado_pais}'
                    
                    logger.info(the_json_logons)
                    
                    #Quitar comentarios en PRO
                    #PRO DYNAMODB
                    wr.dynamodb.put_items(
                        items=[user],
                        table_name='Scoreboard_Usuarios_Bancanet'
                    )
                    
                    #PRO EVENTS
                    event = { 
                        "DetailType": "logons_alerts",
                        "EventBusName": "realtime-integrations",
                        "Source": "bancanet",
                        "Detail": json.dumps(the_json_logons)
                    }
                    
                    # event = { 
                    #     "DetailType": "logons_alerts_dev",
                    #     "EventBusName": "realtime-integrations",
                    #     "Source": "bancanet",
                    #     "Detail": json.dumps(the_json_logons)
                    # }
                    
                    response = events.put_events(Entries=[event])
                else:
                    
                    dispositivo_string = str(the_json_logons["BrowserUserAgent"]).strip()
                    dispositivo_agente = parse(dispositivo_string)
                    dispositivo_light = str(dispositivo_agente)
                    
                    elemento = {
                        "user_agent" : dispositivo_light,
                        "ultimo_login" : fecha_ejecucion
                    }
                    pais = {
                        "pais" : geoip_country,
                        "ultimo_login" : fecha_ejecucion
                    }
                    
                    if geoip_country == "Unidentified" or geoip_country == "Local" :
                        # es un usuario nuevo y pais invalido
                        user = {
                            "usuario": nombre_usuario,
                            "dispositivos": [elemento],
                            "primer_login" : fecha_ejecucion,
                            "ultimo_login": fecha_ejecucion,
                            "paises": []
                        }
                    
                    else:
                        # es un usuario nuevo y pais valido
                        user = {
                            "usuario": nombre_usuario,
                            "dispositivos": [elemento],
                            "primer_login" : fecha_ejecucion,
                            "ultimo_login": fecha_ejecucion,
                            "paises": [pais]
                        }
                    
                    #Quitar comentarios en PRO
                    #PRO DYNAMODB
                    wr.dynamodb.put_items(
                        items=[user],
                        table_name='Scoreboard_Usuarios_Bancanet'
                    )

                    the_json_logons["alerta.paislogon.existentes"] = None
                    the_json_logons["alerta.paislogon.paisdelogon"] = geoip_country
                    the_json_logons["alerta.paislogon.resultado"] = "Usuario Nuevo"
                    
                    
                    the_json_logons["alerta.dispositivo.existentes"] = None
                    the_json_logons["alerta.dispositivo.dispositivologon"] = dispositivo_light
                    the_json_logons["alerta.dispositivo.resultado"] = "Usuario Nuevo"
                    
                    the_json_logons["alerta.descripcion"] = "Usuario Nuevo"
                    the_json_logons["alerta.color"] = "Verde"
                    
                    event = { 
                        "DetailType": "logons_alerts",
                        "EventBusName": "realtime-integrations",
                        "Source": "bancanet",
                        "Detail": json.dumps(the_json_logons)
                    }
                    
                    response = events.put_events(Entries=[event])
        except Exception as e:
            print(e)
            
        
        # Do custom processing on the payload here
        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(bytes(json_output, 'utf-8')).decode('utf-8')
        }
        output.append(output_record)


    return {
        'records': output
    }
    







if __name__ == "__main__" or __name__ == "builtins":
    event = {   
        'invocationId': '3bb4ca23-e83f-4c08-b5b5-9084d3cbb4d6', 
        'deliveryStreamArn': 'arn:aws:firehose:us-east-1:629502476623:deliverystream/bancanet_dbo_auditlog_es_dev', 
        'region': 'us-east-1', 
        'records': [
            # {
            #   "recordId": "49621866908991324304237797940902176265103991578992574466000000",
            #   "approximateArrivalTimestamp": 1657332628255,
            #   "data": "eyJzaW5rX2NvbXBhbnkiOiAiQkxSRyIsICJzaW5rX2Rlc2NyaXB0aW9uIjogImJhbmNhbmV0X3JlZ2lvbmFsX2F1ZGl0bG9nIiwgIkF1ZGl0TG9nSWQiOiAxNzIzMDgyNDkxLCAiQXVkaXREYXRldGltZSI6ICIyMDIyLTA3LTA5VDAyOjEwOjE3Ljg0MzAwMCswMDowMCIsICJBdWRpdFVzZXJJcEFkZHJlc3MiOiAiMjA4Ljg0Ljg1LjU5IiwgIkF1ZGl0RXhlY3V0aW9uTW9kZSI6IDAsICJBdWRpdFNpdGVJZCI6IC0xLCAiQXVkaXRFbGFwc2VkVGltZSI6IDE1LCAiQXVkaXRDb3JyZWxhdGlvbiI6ICIzMTI5ZjY4MS02ZjRlLTQ3ODYtYjFhNC01NDVlOWQ2NjZkNTUiLCAiQXVkaXRTZXJ2aWNlT3BlcmF0aW9uSWQiOiAxNDk2ODgxNzM3LCAiQXVkaXRCcm93c2VyVXNlckFnZW50SWQiOiA0NDA4NzksICJBdWRpdEJ1c2luZXNzQ29ycmVsYXRpb24iOiBudWxsLCAiQXVkaXRBcHByb3ZhbEFjdGlvbklkIjogMCwgIkF1ZGl0VXNlckJyb3dzZXIiOiBudWxsLCAiQXVkaXRVc2VyU2NyZWVuU2l6ZSI6IG51bGwsICJBdWRpdFNlcnZlck1hY0FkZHJlc3MiOiAiMDA1MDU2OUM0RUMxIiwgIkF1ZGl0SG9zdE5hbWVMb2FkU2VydmVyIjogInNlY3VyZS5iYW5jb2xhZmlzZS5jb20iLCAiQXVkaXRIb3N0TmFtZVNlcnZlciI6ICJOSS1DQ0MtQk4tMDMiLCAiQXVkaXRVc2VyQ291bnRyeSI6IG51bGwsICJBdWRpdFVzZXJTZXNzaW9uIjogbnVsbCwgIkNoYW5uZWxJZCI6IDUsICJDaGFubmVsTmFtZSI6ICJNb2JpbGUgQXBwbGljYXRpb25zIiwgIkFjdGlvbklkIjogMCwgIkFjdGlvbk5hbWUiOiAiVW5kZWZpbmVkIiwgIkFjdGlvbkRlc2NyaXB0aW9uIjogIkluZGVmaW5pZGEiLCAiQWN0aW9uUmVzdWx0SWQiOiAxLCAiQWN0aW9uUmVzdWx0RGVzY3JpcHRpb24iOiAiT0siLCAiQnJvd3NlclVzZXJBZ2VudCI6ICJNb3ppbGxhLzUuMCAoTGludXg7IEFuZHJvaWQgMTI7IFNNLUE1MjhCIEJ1aWxkL1NQMUEuMjEwODEyLjAxNjsgd3YpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIFZlcnNpb24vNC4wIENocm9tZS8xMDMuMC41MDYwLjcxIE1vYmlsZSBTYWZhcmkvNTM3LjM2IElDQmFua2luZ1dyYXBwZXIiLCAiU2VydmljZU9wZXJhdGlvbk5hbWUiOiAiR2V0U3Vic2lkaWFyaWVzQ3VzdG9tIiwgIlNlcnZpY2VPcGVyYXRpb25OYW1lc3BhY2UiOiAidXJuOnRhaWxvcmVkLmljYmFua2luZy5zZXJ2aWNlcy5mcmFtZXdvcmsuc3Vic2lkaWFyaWVzLlN1YnNpZGlhcmllc0N1c3RvbVNlcnZpY2UuR2V0U3Vic2lkaWFyaWVzQ3VzdG9tIiwgIlVzZXJJZCI6IG51bGwsICJVc2VyTmFtZSI6IG51bGwsICJVc2VyRnVsbG5hbWUiOiBudWxsLCAiVXNlckVtYWlsIjogbnVsbCwgIlVzZXJQaG9uZSI6IG51bGwsICJNYWluU3Vic2lkaWFyeUlkIjogbnVsbCwgIkNJRl9CYW5jbyI6ICJCTFJHIiwgIkNJRl9OaWNhcmFndWEiOiBudWxsLCAiQ0lGX0Nvc3RhUmljYSI6IG51bGwsICJDSUZfUGFuYW1hIjogbnVsbCwgIkNJRl9Ib25kdXJhcyI6IG51bGwsICJDSUZfUmVwdWJsaWNhRG9taW5pY2FuYSI6IG51bGwsICJ0aW1lc3RhbXAiOiAiMjAyMi0wNy0wOVQwMjoxMDoxNy44NDMwMDArMDA6MDAiLCAicHJvY2Vzc2VkX3RpbWVzdGFtcCI6ICIyMDIyLTA3LTA5VDAyOjEwOjI4LjIzNzQ3NCIsICJpcF9pc29fY29kZSI6IG51bGwsICJpcF9jb3VudHJ5IjogIlVuaWRlbnRpZmllZCIsICJpcF9jaXR5IjogIlVuaWRlbnRpZmllZCIsICJsb2NhdGlvbiI6IHsibGF0IjogbnVsbCwgImxvbiI6IG51bGx9LCAiaXNvX2NvdW50cnkiOiAiVVMiLCAiY291bnRyeSI6ICJFc3RhZG9zIFVuaWRvcyIsICJjb21wYW55IjogIkJMUkciLCAiVXNlclZJUCI6ICJGYWxzZSJ9Cg=="
            # },
            {
              "recordId": "49621866908991324304237797940902176265103991578992574466000000",
              "approximateArrivalTimestamp": 1657332628255,
              "data": "eyJzaW5rX2NvbXBhbnkiOiJCTFJHIiwic2lua19kZXNjcmlwdGlvbiI6ImJhbmNhbmV0X3JlZ2lvbmFsX2F1ZGl0bG9nIiwiQXVkaXRMb2dJZCI6MTc0NjczNDkzMywiQXVkaXREYXRldGltZSI6IjIwMjItMDctMTRUMjI6NDA6MzcuNTQ3MDAwKzAwOjAwIiwiQXVkaXRVc2VySXBBZGRyZXNzIjoiMTkwLjI0Mi4yNS4xMDMiLCJBdWRpdEV4ZWN1dGlvbk1vZGUiOjAsIkF1ZGl0U2l0ZUlkIjo0NjMyODcsIkF1ZGl0RWxhcHNlZFRpbWUiOjIzNCwiQXVkaXRDb3JyZWxhdGlvbiI6ImJkYjU2YWU5LWQyM2EtNGFmMC05ZjU0LWE0YjIwNjQzZjI3MiIsIkF1ZGl0U2VydmljZU9wZXJhdGlvbklkIjoxMDA4MTk1MzEsIkF1ZGl0QnJvd3NlclVzZXJBZ2VudElkIjo0MTQ4MjIsIkF1ZGl0QnVzaW5lc3NDb3JyZWxhdGlvbiI6bnVsbCwiQXVkaXRBcHByb3ZhbEFjdGlvbklkIjowLCJBdWRpdFVzZXJCcm93c2VyIjoiQ0hST01FIiwiQXVkaXRVc2VyU2NyZWVuU2l6ZSI6IjExNTJYODY0IiwiQXVkaXRTZXJ2ZXJNYWNBZGRyZXNzIjoiMDA1MDU2OUNEOTg5IiwiQXVkaXRIb3N0TmFtZUxvYWRTZXJ2ZXIiOiJzZWN1cmUuYmFuY29sYWZpc2UuY29tIiwiQXVkaXRIb3N0TmFtZVNlcnZlciI6Ik5JLUNDQy1CTi0wMSIsIkF1ZGl0VXNlckNvdW50cnkiOiJDb2xvbWJpYSIsIkF1ZGl0VXNlclNlc3Npb24iOiJIeDFNVU14Mmx5MUtIK3VuZnliTDV6UVlGYkxIcnpiZFBsWm1HaUVXKzVFYVlhQW1POFE4dUlUalhRbi9Oc1dURFRTY0YxSDcyeDNEUW5PVlZ4VUpJcjEzMVZPYk5qQVB6YlpxIiwiQ2hhbm5lbElkIjoxLCJDaGFubmVsTmFtZSI6IkJhbmtpbmcgV2ViIiwiQWN0aW9uSWQiOjEsIkFjdGlvbk5hbWUiOiJMb2dPbiIsIkFjdGlvbkRlc2NyaXB0aW9uIjoiSW5ncmVzbyBhbCBzaXN0ZW1hIiwiQWN0aW9uUmVzdWx0SWQiOjEsIkFjdGlvblJlc3VsdERlc2NyaXB0aW9uIjoiT0siLCJCcm93c2VyVXNlckFnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwMy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiU2VydmljZU9wZXJhdGlvbk5hbWUiOiJMb2dPbkN1c3RvbSIsIlNlcnZpY2VPcGVyYXRpb25OYW1lc3BhY2UiOiJ1cm46dGFpbG9yZWQuaWNiYW5raW5nLnNlcnZpY2VzLmFkbWluaXN0cmF0aW9uLmdlbmVyYWwuR2VuZXJhbEN1c3RvbVNlcnZpY2UuTG9nT25DdXN0b20iLCJVc2VySWQiOjQ3NzE3NiwiVXNlck5hbWUiOiJubXVycmF5OTkyNTI5NzgiLCJVc2VyRnVsbG5hbWUiOiJOZXN0b3IgIFJvYmVydG8gTXVycmF5ICBRdWlqYWRhIiwiVXNlckVtYWlsIjoibmVzdG9yLm11cnJheUBnbWFpbC5jb20iLCJVc2VyUGhvbmUiOiI1MDRAOTkyNTI5NzgiLCJNYWluU3Vic2lkaWFyeUlkIjo0LCJDSUZfQmFuY28iOiJCTEhOIiwiQ0lGX05pY2FyYWd1YSI6MCwiQ0lGX0Nvc3RhUmljYSI6MCwiQ0lGX1BhbmFtYSI6MCwiQ0lGX0hvbmR1cmFzIjoxLCJDSUZfUmVwdWJsaWNhRG9taW5pY2FuYSI6MCwidGltZXN0YW1wIjoiMjAyMi0wNy0xNFQyMjo0MDozNy41NDcwMDArMDA6MDAiLCJwcm9jZXNzZWRfdGltZXN0YW1wIjoiMjAyMi0wNy0xNFQyMjo0MDo1OC42MjM5MzQiLCJpcF9pc29fY29kZSI6IkhOIiwiaXBfY291bnRyeSI6IkhvbmR1cmFzIiwiaXBfY2l0eSI6IlVuaWRlbnRpZmllZCIsImxvY2F0aW9uIjp7ImxhdCI6MTUuMCwibG9uIjotODYuNX0sImlzb19jb3VudHJ5IjoiVVMiLCJjb3VudHJ5IjoiRXN0YWRvcyBVbmlkb3MiLCJjb21wYW55IjoiQkxSRyIsIlVzZXJWSVAiOiJGYWxzZSIsImFsZXJ0YS5wYWlzbG9nb24uZXhpc3RlbnRlcyI6W3sidWx0aW1vX2xvZ2luIjoiMjAyMi0wMi0xNSAyMzo1Mjo1OC4zNzcwMDAiLCJwYWlzIjoiSG9uZHVyYXMifV0sImFsZXJ0YS5kaXNwb3NpdGl2by5leGlzdGVudGVzIjpbeyJ1c2VyX2FnZW50IjoiUEMgLyBXaW5kb3dzIDEwIC8gQ2hyb21lIDk4LjAuNDc1OCIsInVsdGltb19sb2dpbiI6IjIwMjItMDItMTVUMjM6NTI6NTguMzc3MDAwIn1dLCJhbGVydGEuZGlzcG9zaXRpdm8ucmVzdWx0YWRvIjoiQWN0dWFsaXphZG8iLCJhbGVydGEucGFpc2xvZ29uLnJlc3VsdGFkbyI6IkV4aXN0ZW50ZSIsImFsZXJ0YS5jb2xvciI6IlZlcmRlIiwiYWxlcnRhLnBhaXNsb2dvbi5wYWlzZGVsb2dvbiI6IkhvbmR1cmFzIiwiYWxlcnRhLmRpc3Bvc2l0aXZvLmRpc3Bvc2l0aXZvbG9nb24iOiJQQyAvIFdpbmRvd3MgMTAgLyBDaHJvbWUgMTAzLjAuMCIsImFsZXJ0YS5kZXNjcmlwY2lvbiI6IkRpc3Bvc2l0aXZvIEFjdHVhbGl6YWRvIHkgUGFpcyBFeGlzdGVudGUifQ=="
            }
        ]
    }
    context = []
    lambda_handler(event, context)