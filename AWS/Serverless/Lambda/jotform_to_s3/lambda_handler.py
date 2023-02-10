#https://www.jotform.com/build/212595160036855/publish#preview

import json
import requests
import os
import boto3
from botocore.exceptions import ClientError
import logging

# Declaring and initialzing variables
s3_client = boto3.client('s3')
secrets_client = boto3.client('secretsmanager')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Environment variables
secret_name = os.environ['SECRET_NAME']
region_name = os.environ['REGION']
bucket_name = os.environ['BUCKET_NAME']

def get_secret_string():
    try:
        secret = secrets_client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        logger.info(e)
        return f"{secret_name} secret can not be obtained: \n{e}"
    
    credentials = secret['SecretString']
    json_credentials = json.loads(credentials)
    api_key_jotform =json_credentials["api_key"]
    logger.info(api_key_jotform)
    return api_key_jotform
    
def extract_json_jotform(submission_id):
    try:
        request_api_jotform = requests.get(f"https://api.jotform.com/submission/{submission_id}?apiKey={get_secret_string()}")
        logger.info(request_api_jotform)
        data = json.loads(request_api_jotform.content.decode('utf-8'))["content"]["answers"]
        data_items = data.items()
    except ClientError as e:
        logger.info(e)
        return f"{submission_id} is not a valid submissionID: \n{e}"
    key_list = []
    value_list = []
    for item in data_items:
        if "answer" in item[1]:
            key_list.append(item[1]["name"])
            value_list.append(item[1]["answer"])
        else:
            key_list.append(item[1]["name"])
            value_list.append(None)

    JSON_formatted_data = dict(zip(key_list, value_list))
    return JSON_formatted_data

def lambda_handler(event, context):
    logger.info("Data In: {}".format(json.dumps(event)))
    form_data = event['body']
    form_data_index_string = form_data.find("submissionID") + 17
    submissionId = int(form_data[form_data_index_string:form_data_index_string + 19])
    print(submissionId)
    print(type(submissionId))
    data = extract_json_jotform(submissionId)
    data_json = json.dumps(data, indent=4, sort_keys=True)
    logger.info(data_json)
    s3_client.put_object(Body=str(data_json), Bucket=bucket_name, Key='jotform_data.json')

    return {
        'statusCode': 200,
        'body': 'OK'
    }