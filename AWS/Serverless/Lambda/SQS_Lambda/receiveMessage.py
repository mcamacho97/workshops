import boto3

def lambda_handler(event, context):
    queue_url = 'https://sqs.us-east-1.amazonaws.com/669611188524/sendDataSQS'
    for record in event['Records']:
        messageid = record['messageId']
        print(str(messageid))
        receipt_handle = record['receiptHandle']
        print(str(receipt_handle))
        CLI_Selfie = record["messageAttributes"]['CLI_Selfie']['stringValue']
        CLI_CaraDelantera = record["messageAttributes"]['CLI_CaraDelantera']['stringValue']
        CLI_CaraTrasera = record["messageAttributes"]['CLI_CaraTrasera']['stringValue']
        print(str(CLI_Selfie))
        print(str(CLI_CaraDelantera))
        print(str(CLI_CaraTrasera))