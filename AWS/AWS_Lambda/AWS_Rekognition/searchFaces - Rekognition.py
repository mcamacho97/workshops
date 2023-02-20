import json
import logging
import boto3
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def search_faces(collectionId, bucket, photo, threshold, maxFaces):
    client=boto3.client('rekognition')

    response=client.search_faces_by_image(CollectionId=collectionId,
                                Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                FaceMatchThreshold=threshold,
                                MaxFaces=maxFaces)
    
    faceMatches=response['FaceMatches']
    results = '0%'
    try:
        for match in faceMatches:
            print ('FaceId:' + match['Face']['FaceId'])
            print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
            results = match['Similarity']
            return results

    except Exception as e:
        logger.error('exception: {}' .format(e))
        exceptionDetail = e
        return results

            
def get_s3_objects_names(bucket):
    s3 = boto3.client('s3')
    objectsname = []
    response = s3.list_objects_v2(Bucket=bucket)
    for bucket in response['Contents']:
        objects = bucket['Key']
        objectsname.append(objects)
    return objectsname

def lambda_handler(event, context):
    print(event)
    body = json.loads(event['body'])
    # New variables with API
    collectionId = os.environ['COLLECTION_ID']
    bucket = os.environ['BUCKET']
    threshold = int(os.environ['THRESHOLD'])
    maxFaces = int(os.environ['MAX_FACES'])
    photo = body['key']

    search_faces_count = search_faces(collectionId, bucket, photo, threshold, maxFaces)

    #Construct the body of the response object
    searchFacesResponse = {}
    searchFacesResponse['collectionId'] = f'Collection Id: {collectionId}'
    searchFacesResponse['bucket'] = f'The bucket name is {bucket}'
    searchFacesResponse['photo'] = f'The photo name uploaded is {photo}'
    searchFacesResponse['threshold'] = f'Threshold: {threshold}'
    searchFacesResponse['maxfaces'] = f'Max faces in the photo: {maxFaces}'
    searchFacesResponse['message'] = f'Results of similarity: {search_faces_count}'
    searchFacesResponse['result'] = 'YES' if int(search_faces_count or 0) > threshold else 'NO'

    #Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    }
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(searchFacesResponse)
    
    return responseObject
