import requests
import boto3
from botocore.session import Session
from requests_aws4auth import AWS4Auth

# This is the URL of the API Gateway endpoint.
api_url = "https://dvcoymvmu7.execute-api.us-east-1.amazonaws.com/v1/safedelete"

# Creating a dictionary with a key called `s3_path` and a value of
# `s3://trainingbi-lafise/bancanet/batch/dbo/catteceros/dt=2022-08-09`.
s3_path_delete = {
    "s3_path": "s3://trainingbi-lafise/bancanet/batch/dbo/catteceros/dt=2022-08-09"}

# Getting the credentials from the current session.
credentials = boto3.Session().get_credentials()

# Creating an object that will be used to authenticate the request.
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,
                   'us-east-1', 'execute-api', session_token=credentials.token)

# Sending a DELETE request to the API Gateway endpoint.
response = requests.delete(url=api_url, auth=awsauth, json=s3_path_delete)
print(response.text)
