import boto3

# Create SQS client
sqs = boto3.client('sqs')

queue_url = 'https://sqs.us-east-1.amazonaws.com/669611188524/sendDataSQS'


def lambda_handler(event, context):
    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes={
            'CLI_Selfie': {
                'DataType': 'String',
                'StringValue': 'selfie.jpg'
            },
            'CLI_CaraDelantera': {
                'DataType': 'String',
                'StringValue': 'documento.jpg'
            },
            'CLI_CaraTrasera': {
                'DataType': 'Number',
                'StringValue': '10'
            }
        },
        MessageBody=(
            'Esto es una prueba para enviar data de un lambda a otro'
        )
    )
    
    return response['MessageId']