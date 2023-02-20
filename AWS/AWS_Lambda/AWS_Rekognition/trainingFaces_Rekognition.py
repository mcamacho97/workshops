import boto3
import json

global bucket
global collection_id
global test
def add_faces_to_collection(bucket,photo,collection_id):
    client=boto3.client('rekognition')
    response=client.index_faces(CollectionId=collection_id,
                                Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                ExternalImageId=photo,
                                MaxFaces=1,
                                QualityFilter="AUTO",
                                DetectionAttributes=['ALL'])

    print ('Results for ' + photo) 	
    print('Faces indexed:')						
    for faceRecord in response['FaceRecords']:
         print('  Face ID: ' + faceRecord['Face']['FaceId'])
         print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)
    return len(response['FaceRecords'])
    
def get_s3_objects_names():
    bucket = "trainingfacecollection-809489680864"
    s3 = boto3.client('s3')
    objectsname = []
    response = s3.list_objects_v2(Bucket=bucket)
    for bucket in response['Contents']:
        objects = bucket['Key']
        objectsname.append(objects)   #optional if you have more filefolders to got through.
    return objectsname

def lambda_handler(event, context):
    bucket = "trainingfacecollection-809489680864"
    collection_id = "robert"
    listPhoto = get_s3_objects_names()

    for photo in listPhoto:
        indexed_faces_count = add_faces_to_collection(bucket, photo, collection_id)

    return {
        'statusCode': 200,
        'body': json.dumps("Faces indexed count: " + str(indexed_faces_count))
    }
