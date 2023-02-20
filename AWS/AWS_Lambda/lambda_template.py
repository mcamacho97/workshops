import json

#Event JSON payload - API Gateway
event  =  {
    "resource": "/example ",
    "path": "/example ",
    "httpMethod": "POST",
    "body": "JSON ESCAPE"
}

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

if __name__ == "__main__":
    lambda_handler(event, None)
