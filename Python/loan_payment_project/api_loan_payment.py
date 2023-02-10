# Referencia
# Video de Polanco: https://drive.google.com/file/d/1wIEXy3EOW3ZN2Z60HtDCPyEyy6ymA1iN/view
# Código de Maurizzio: https://replit.com/@mpenalba/LoanPaymentCalculator#main.py

# Import Libraries
import json
from datetime import datetime
from pytz import timezone

# Event JSON payload
event = {
    "resource": "/transactions ",
    "path": "/transactions ",
    "httpMethod": "POST",
    "body": "{\r\n  \"month_installments\": 12,\r\n  \"payment_day1\": 10,\r\n  \"payment_day2\": 25,\r\n  \"loan_amount\": 20000\r\n}"
    # "body": "{\r\n  \"month_installments\": 12,\r\n  \"payment_day1\": 10,\r\n  \"loan_amount\": 20000\r\n}"
}

today = datetime.today()
global payment_day1
global payment_day2
global loan_payment_response


def lambda_handler(event, context):
    loan_payment_response = {}

    body = json.loads(event['body'])
    # 1 Parse out query string parameter
    month_installments = body['month_installments']
    loan_amount = body['loan_amount']
    payment_day1 = body['payment_day1']
    interest_rate = 0.46
    opening_date = today.strftime("%Y-%m-%d")

    # Calculate balance

    # 2 Construct the body of the response object
    loan_payment_response['month_installments'] = month_installments
    loan_payment_response['loan_amount'] = loan_amount
    loan_payment_response['payment_day1'] = payment_day1
    if "payment_day2" in body:
        payment_day2 = body['payment_day2']
        loan_payment_response['payment_day2'] = payment_day2
    loan_payment_response['interest_rate'] = interest_rate
    loan_payment_response['opening_date'] = opening_date

    # 3 Construct http response object
    response_object = {}
    response_object['statusCode'] = 200
    response_object['headers'] = {}
    response_object['headers']['Content-Type'] = 'application/json'
    response_object['body'] = json.dumps(loan_payment_response)

    # 4 Return the response object
    print(response_object)
    return response_object


if __name__ == "__main__":
    lambda_handler(event, None)
