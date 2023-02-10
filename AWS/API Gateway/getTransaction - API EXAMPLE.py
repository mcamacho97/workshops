import json

event  =  {
    "resource": "/example",
    "path": "/example",
    "httpMethod": "GET",
    "queryStringParameters": {
        "transactionId":"121212",
        "type": "prueba",
        "amount": "20000"
    },
}


def lambda_handler(event, context):
    
# Getting the query string parameters from the event object.
    transactionId = event['queryStringParameters']['transactionId']
    transactionType = event['queryStringParameters']['type']
    transactionAmount = event['queryStringParameters']['amount']

# Creating a dictionary with the keys and values that you want to return.
    transactionResponse = {}
    transactionResponse['transactionId'] = transactionId    
    transactionResponse['type'] = transactionType    
    transactionResponse['amount'] = transactionAmount
    transactionResponse['message'] = 'GET TRANSACTION WORKS'


# This is the response object that is returned to the client.
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(transactionResponse)

    print  (responseObject)
    return responseObject

if __name__ == "__main__":
    lambda_handler(event, None)