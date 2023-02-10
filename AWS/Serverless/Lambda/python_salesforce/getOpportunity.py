import boto3
from botocore.exceptions import ClientError
import json
import logging
import os
import urllib3

# Declaring and initialzing variables
http = urllib3.PoolManager()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
secrets_client = boto3.client('secretsmanager')
client_id = 'client_id'
client_secret = 'client_secret'
user_name = 'username'
password = 'password'
region_name = "us-east-1"

def get_token_URL(secret_name):
    """
    It takes a token, an endpoint URL, and a list of fields, and returns a dictionary with the data and
    status of the response
    
    :param secret_name: The name of the secret in Secrets Manager
    :return: A dictionary with two keys: data and status.
    """
    try:
        secret = secrets_client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        logger.info(e)
        return f"{secret_name} secret can not be obtained: \n{e}"

    credentials = secret['SecretString']

    json_credentials = json.loads(credentials)

    auth_response = http.request('POST', json_credentials['auth_url'], fields={
        client_id: json_credentials[client_id],
        client_secret: json_credentials[client_secret],
        'grant_type': password,
        user_name: json_credentials[user_name],
        password: json_credentials[password]
    })

    json_Response = json.loads(auth_response.data.decode("utf-8"))
    object_URL = json_Response['instance_url'] + \
        os.environ['OPP_ENDPOINT']
    return [json_Response['access_token'], object_URL]

def get_opportunityById(token, endpoint_URL, fields):
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json'
    }

    response = http.request('GET', endpoint_URL, headers=headers)
    response_decoded =  json.loads(response.data.decode("utf-8"))
    logger.info(response_decoded)
    
    if fields in response_decoded:
        return {'data': response_decoded[fields], 'status': response.status}
    else:
        return {'data': response_decoded, 'status': response.status}

def lambda_handler(event, context):

    opp_id = event['queryStringParameters']['opportunityId']
    fields = event['queryStringParameters']['fields']
    response = get_token_URL(os.environ['SALESFORCE_SECRET_NAME'])
    if isinstance(response, list):
        [token, object_URL] = response
    else:
        return response

    #Creating the full url with the opportunity id    
    full_URL = f'{object_URL}/{opp_id}'    

    opportunity_response = get_opportunityById(token, full_URL, fields)
    response_object = {}
    response_object['statusCode'] = 200
    response_object['headers'] = {}
    response_object['headers']['Content-Type'] = 'application/json'
    response_object['headers']['Access-Control-Allow-Headers'] = 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
    response_object['headers']['Access-Control-Allow-Origin'] = '*'
    response_object['headers']['Access-Control-Allow-Methods'] = 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT'
    response_object['body'] = json.dumps(opportunity_response)
    
    return response_object

