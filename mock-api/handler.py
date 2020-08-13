import json
import os
import logging
import boto3
from botocore.exceptions import ClientError

def get_data(entry):
    """ Gets the data from the DynamoDB entry """
    response = {
        'response': 'No Data'
    }
    if 'Data' in entry:
        response = entry['Data']
    return json.dumps(response)

def request(event, context):
    """ Handles all requests coming into the API Gateway """
    hostname = event['headers']['Host']
    path = event['path']

    dynamodb_resource = boto3.resource('dynamodb')
    dynamodb_table = dynamodb_resource.Table(os.environ['MOCKAPI_TABLE'])

    # Default response is to return a 404 error
    response = {
        "statusCode": 404,
        "body": json.dumps({
            "Errors": [
                "page not found"
            ],
            "Path": path,
            "Hostname": hostname
        })
    }

    try:
        # Attempt to retrieve an item from the DynamoDB table
        dynamodb_result = dynamodb_table.get_item(Key={
            'Hostname': hostname,
            'Path': path
        })
    except ClientError as e:
        # Log the error message to cloudwatch
        logging.info(e.response['Error']['Message'])
    else:
        if 'Item' in dynamodb_result:
            entry = dynamodb_result['Item']
            # Check if authentication is required
            if 'Auth' in entry and entry['Auth']:
                # Check if Authorization header is there and 
                # if so, return data (we don't validate the token though)
                if 'Authorization' in event['headers']:
                    response = {
                        "statusCode": 200,
                        "body": get_data(entry)
                    }
                # Otherwise return a standard access denied response.
                else:
                    response = {
                        "statusCode": 401,
                        "body":  json.dumps({
                            "Errors": [
                                "This resource requires authorization to access"
                            ]
                        })
                    }
            # If no auth is required, then just dump data
            else:
                response = {
                    "statusCode": 200,
                    "body": get_data(entry)
                }

    return response
