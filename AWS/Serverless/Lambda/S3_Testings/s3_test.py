import json
import boto3

s3 = boto3.client('s3')
def list_bucket():
    response = s3.list_buckets()['Buckets']
    for bucket in response:
        print(bucket['Name'])

def list_objects():
    response = s3.list_objects_v2(Bucket="trainingfacecollection-809489680864")
    for bucket in response['Contents']:
        print(bucket['Key'])

def lambda_handler(event, context):
    # TODO implement
    return list_objects()