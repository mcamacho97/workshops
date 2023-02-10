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
    It takes a secret name and an opportunity id as parameters, and returns a list containing the access
    token and the full URL to the opportunity

    :param secret_name: The name of the secret in Secrets Manager
    :return: A list of two items:
    1. The access token
    2. The object URL
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


def create_opportunity_id(data, token, endpoint_URL):
    for key in data:
        if 'data' in key.lower():
            data[key] = json.dumps(data[key])

    encodedData = json.dumps(data)

    print(encodedData)

    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json'
    }

    response = http.request("PATCH", endpoint_URL,
                            body=encodedData, headers=headers)
    return {'data': json.loads(response.data.decode("utf-8")) if response.data else "No Response Data", 'status': response.status}


def lambda_handler(event, context):
    response = {'statusCode': 400,
                "headers": {
                    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                    "Access-Control-Allow-Origin": '*',
                    'Access-Control-Allow-Methods': 'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT'},
                "body": "Error durante la peticion hacia salesforce"}

    body = json.loads(event['body'])
    opprtunity_id = body['id']
    oppportunity_data = body['data']

    
    response_get_token_url = get_token_URL(os.environ['SALESFORCE_SECRET_NAME'])  
    if isinstance(response_get_token_url, list):
        [token, object_URL] = response_get_token_url
    else:
        return response_get_token_url

    # Creating the full url with the opportunity id
    full_URL = f'{object_URL}/{opprtunity_id}'

    salesforce_response = create_opportunity_id(oppportunity_data, token, full_URL)

    if salesforce_response["status"] == 204:
        response['statusCode'] = 200
        response['body'] = json.dumps(salesforce_response)
        return response
    else:
        return response