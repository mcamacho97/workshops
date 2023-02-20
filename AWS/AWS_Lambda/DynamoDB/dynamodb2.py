import json
import boto3
import os
import logging
import random
import requests

from geopy import distance

# Function is called as part of the "Get Unicorn Location" step of the Step Function orchestrator workflow.
# This is called once for every Unicorn in your fleet.
# The output of the function is stored under the "UnicornLocation" key in the Step Function workflow.
# Check the step input and output for this Step Function step to see this.
# Check these steps for logs when exploring and troubleshooting.
# 
# Sample event triggering this Lambda function. Data is sample data only
# This will help you to test the function in the console and help troubleshoot
# {
#   "Destination": {
#     "latitude": 36.10017698780685,
#     "longitude": -115.25210817712863
#   },
#   "Unicorn": {
#     "capacity": "1",
#     "isSpot": "False",
#     "unicorn-id": "5aac718e-e80a-494e-afd4-13c5493cfdbd",
#     "status": "available",
#     "unicorn-name": "Shimmering Mauve Nose",
#     "team-id": "12398172398172398173",
#     "freeAtTime": "2021-10-22T10:32:03",
#     "type": "walking"
#   },
#   "RidePassengers": 3,
#   "RideId": "b101f179-1a5d-4651-a5b5-442b3fb36a50",
#   "TeamId": "12398172398172398173",
#   "Source": {
#     "latitude": 36.09625997410361,
#     "longitude": -115.24385996414345
#   }
# }

logger = logging.getLogger()
logger.setLevel(logging.INFO)

unicornsTableName = "UnicornLocations"

dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
table = dynamodb.Table(unicornsTableName)

def lambda_handler(event, context):
    logger.debug(event)

    unicornId = event["Unicorn"]["unicorn-id"]
    source_loc = event["Source"] # The source location of the ride request
    
    # Retrieve the location for unicorn from DynamoDb 
    response = table.get_item(
       Key= { 'unicorn-id' :unicornId } 
        )

    if 'Item' in response:
        unicorn = response['Item']
        unicorn_loc = { "latitude": unicorn["latitude"], "longitude": unicorn["longitude"] }

        # This always seems to be coming back empty???
        # TODO - looks like the DynamoDb table with locations is completely empty :(
        # We have a stream of location information coming into IOT Core on the topic 'iot/unicorns' - need to get this into DynamoDb table somehow.
        #for item in unicorn:
        #    unicorn_loc = { "latitude": unicorn["latitude"], "longitude": unicorn["longitude"] }
        #    newItem['latitude']['N'] = item['latitude']
        #    newItem['longitude']['N'] = item['longitude']
        #    client.put_item(TableName="UnicornLocations", Item=newItem)
        logger.info("Unicorn {} is at {},{}".format(unicornId,unicorn["latitude"],unicorn["longitude"]))

    else:
        logger.info("Could not find unicorn location :( - returning hardcoded values")
        unicorn_loc = {"latitude": 36.14172955400423,"longitude": -115.00183110019223}
        # While we don't have the locations available, just return a static location
        #unicorn_loc = {"latitude": {'S':36.14172955400423},"longitude": {'S':-115.00183110019223}} # eh, all the unicorns are in Las Vegas.  Close enough.
        #newItem['latitude']['S'] = unicorn_loc['latitude']
        #newItem['longitude']['S'] = unicorn_loc['longitude']
        #dynamodb.put_item(TableName='fruitSalad', Item={'fruitName':{'S':'Banana'},'key2':{'N':'value2'}})

        #client.put_item(TableName="UnicornLocations", Item={"latitude": {'N':'36.14172955400423'},"longitude": {'N':'-115.00183110019223'}})        

        
    # Distance from the unicorn to source of ride. 
    # This is used to determine how far each unicorn is from the ride source for ordering

    distance_in_miles = distance.distance( (unicorn_loc['latitude'],unicorn_loc['longitude']) , (source_loc['latitude'],source_loc['longitude']) ).miles


    location = {}
    location['Location'] = unicorn_loc
    location['DistanceToRide'] = distance_in_miles

    return location


--------------------------------------------------------------------------------------------------
import json
import urllib.parse
import urllib.request
import boto3
import logging
import os
import requests

# Function is called as part of the "Get Unicorns" step of the Step Function orchestrator workflow
# The output from the function is then stored in under the key "Unicorns" in the Step Function execution.
# Check these steps for logs when exploring and troubleshooting
# 
# The output is then used in the "Are there any Unicorns" decision step in the Step Function to determine
# if there are unicorns in your fleet. The information about Unicorns is then used throughout the rest of the 
# Step Function logic.
# 
# Sample event triggering this Lambda function. Data is sample data only
# This will help you to test the function in the console and help troubleshoot
# {
#     "Destination": {
#       "latitude": 36.10017698780685,
#       "longitude": -115.25210817712863
#     },
#     "Customer": {
#       "CustomerEmail": "sampledata_fmcdaniel@yahoo.com",
#       "CustomerIpAddress": "118.61.148.135",
#       "CustomerId": "fad1e103-6cef-1e5c-18cf-3c4dba7f9e53"
#     },
#     "ConfirmationTTL": "5",
#     "RideId": "b101f179-1a5d-4651-a5b5-442b3fb36a50",
#     "NumberOfPassengers": 3,
#     "Source": {
#       "latitude": 36.09625997410361,
#       "longitude": -115.24385996414345
#     },
#     "TeamId": "12398172398172398173"
#   }

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ssm = boto3.client('ssm')

# Get the API key for calling the central API service from HQ to get list of all our unicorns
# Helpfully, they provided this information in some Environment Variables and Systems Manager Parameter Store values!
api_key_param_id = os.environ.get('UNICORNS_API_TOKEN_PARAM_ID')
api_key_ssm_param = ssm.get_parameter(Name=api_key_param_id)
team_api_key = api_key_ssm_param['Parameter']['Value']

def lambda_handler(event, context):
    logger.info("Getting unicorns in fleet")

    team_id = event['TeamId']

    # The address for unicorn-api.unicorn.rentals is stored in a Private Hosted Zone in Route 53 which this Lambda function has access to
    # Management have said something about possible network issues with this address when they install their new IOT-connected kitchen equipment
    # Apparently either the unicorn-api or the smart-teapot address should always be working
    # We should look into setting up a Route 53 Healthcheck to make sure we can Failover to the teapot address if the unicorn-api one is not available

    url =  f"http://unicorn-api.unicorn.rentals/team/{team_id}/unicorns"
    headers = {'x-api-key': team_api_key}

    r = requests.get(url, headers=headers)
    logger.info(f'StatusCode - {r.status_code}')
    logger.info(r.text)

    if r.status_code != 200:
        logger.info("Could not communicate with API server!")
        raise Exception('Could not communicate with API server!', r.text)

    return json.loads(r.text)

    
    # returns unicorns in the format
    # [
    #   {
    #     "capacity": "1",
    #     "isSpot": "0",
    #     "unicorn-id": "0a1dba22-538c-4528-8495-a594e54e689d",
    #     "status": "busy",
    #     "unicorn-name": "Glittering Violet Star",
    #     "team-id": "24eec976eca648eab61514b241032041",
    #     "type": "walking"
    #   },
    #   {
    #     "isSpot": "0",
    #     "capacity": "1",
    #     "unicorn-id": "19a08718-b95d-4d0e-9ec4-c3802ac7907b",
    #     "status": "available",
    #     "unicorn-name": "Sparkly Pink Princess",
    #     "team-id": "24eec976eca648eab61514b241032041",
    #     "type": "walking"
    #   },
    #   {
    #     "isSpot": "0",
    #     "capacity": "1",
    #     "unicorn-id": "1eaf72ce-01b7-4441-bc38-54ccd32da600",
    #     "status": "available",
    #     "unicorn-name": "Glittering Golden Raindrop",
    #     "team-id": "24eec976eca648eab61514b241032041",
    #     "type": "walking"
    #   }
    # ]