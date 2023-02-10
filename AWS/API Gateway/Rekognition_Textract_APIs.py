# This is importing the libraries that are needed for the lambda function to work.
import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#object_name="rekognition/NI/Test.jpg"
#object_name=""

def detect_text_Rekognition(photo, bucket, numDocumento):
    """
    A function that detects text in an image.
    
    :param photo: the name of the image file
    :param bucket: the name of the bucket where the image is stored
    :param numDocumento: is the name of the file that is being processed
    """

    rekognition=boto3.client('rekognition')
    response=rekognition.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
                        
    textDetections=response['TextDetections']
    result = False
    for text in textDetections:
        detectedText = str(text['DetectedText']).replace(' ','').replace('-','')
        if (numDocumento in detectedText):
            result = True
        else:
            result
            #print ('Type:' + text['Type']) TIPO LINE
    return ('El resultado es',result)
    
#Función para detectar texto con Amazon Textract    
def detect_text_Textract(photo, bucket, numDocumento):
    # Amazon Textract client
    textract = boto3.client('textract')
    
    # Call Amazon Textract
    response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': bucket,
                'Name': photo
            }
        })
    
    #print(response)
    
    # Print detected text
    result = False
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            detectedText = str(item["Text"]).replace(' ','').replace('-','')
            if (numDocumento in detectedText):
                result = True
            else:
                result
            #print ('Type:' + text['Type']) TIPO LINE
    return ('El resultado es',result)
        

def lambda_handler(event, context):
    """
    A function that is called when the lambda function is triggered.
    
    :param event: This is the event that triggered the lambda function. In this case, it's the API
    Gateway
    :param context: This is an object that contains methods and properties that provide information
    about the invocation, function, and execution environment
    """
    print(event)
    bucket = 'lafise-labs'
    
    path = event['path']
    
# Checking the path of the request and then it is parsing the body of the request.
    if path == "/rekognition":
        body = json.loads(event['body'])
        object_name = body['object_name']
        num_documento = body['num_documento']
        
        return {
            'statusCode': 200,
            'body': json.dumps(detect_text_Rekognition(object_name, bucket, num_documento))
        }        
    elif path == "/textract":
        body = json.loads(event['body'])
        object_name = body['object_name']
        num_documento = body['num_documento']
        
        return {
            'statusCode': 200,
            'body': json.dumps(detect_text_Textract(object_name, bucket, num_documento))
        }   


    



