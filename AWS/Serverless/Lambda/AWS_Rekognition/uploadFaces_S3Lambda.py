import boto3
import json 
import os
import logging
from botocore.client import Config
import random

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def signedUrl(bucket, key):
    s3 = boto3.client('s3', config=Config(signature_version='s3v4'))
    url = s3.generate_presigned_url(
    ClientMethod='put_object', 
    Params={'Bucket': bucket, 'Key': key},
    ExpiresIn=3600)
    return url

def lambda_handler(event, context):
    bucket = 'searchfaces-809489680864'
    key = '{}.jpeg'.format(random.randint(0,100000))
    
    #1 Construct the body of the response object
    signedUrlResponse = {}
    signedUrlResponse['bucket'] = bucket    
    signedUrlResponse['key'] = key
    response = signedUrl(bucket, key)
    signedUrlResponse['uploadURL'] = response

    #2 Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    }
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(signedUrlResponse)
    
    return responseObject