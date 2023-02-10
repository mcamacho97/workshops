import json

#Event JSON payload
event  =  {
    "resource": "/transactions ",
    "path": "/transactions ",
    "httpMethod": "POST",
    "body": "{\r\n    \"type\": \"PURCHASE\",\r\n    \"amount\": 500,\r\n    \"updateAmount\": 200\r\n}"
}

def lambda_handler(event, context):

    body = json.loads(event['body'])
    #1 Parse out query string parameter
    transactionId = 10
    transactionType = body['type']
    transactionAmount = body['amount']
    updateAmount = body['updateAmount']
    #Calculate the old amount with the new amount
    result = transactionAmount + updateAmount

    #2 Construct the body of the response object
    transactionResponse = {}
    transactionResponse['transactionId'] = transactionId    
    transactionResponse['type'] = transactionType    
    transactionResponse['amount'] = transactionAmount
    transactionResponse['updateAmount'] = updateAmount
    transactionResponse['message'] = f'The new amount is {result}'

    #3 Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(transactionResponse)
    
    #4 Return the response object
    print  (responseObject)
    return responseObject

if __name__ == "__main__":
    lambda_handler(event, None)