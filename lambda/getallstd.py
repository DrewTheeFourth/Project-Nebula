import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Initialize a DynamoDB resource object for the specified region
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    # Select the DynamoDB table named 'Students'
    table = dynamodb.Table('Students')  # Update to the correct table name

    # Extract query parameters
    email = event.get('queryStringParameters', {}).get('Email')
    name = event.get('queryStringParameters', {}).get('Name')

    try:
        if email and name:
            # Query the table to retrieve the specific item
            response = table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('Email').eq(email) & 
                                       boto3.dynamodb.conditions.Key('Name').eq(name)
            )
            data = response['Items']

            # If no items are found, return an appropriate message
            if not data:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'message': 'Item not found.'})
                }

            # Return the retrieved data
            return {
                'statusCode': 200,
                'body': json.dumps(data)
            }
        
        else:
            # Scan the table to retrieve all items
            response = table.scan()
            data = response['Items']

            # If there are more items to scan, continue scanning until all items are retrieved
            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                data.extend(response['Items'])

            # Return the retrieved data
            return {
                'statusCode': 200,
                'body': json.dumps(data)
            }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
