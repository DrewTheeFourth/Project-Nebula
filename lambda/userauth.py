import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Initialize a DynamoDB resource object for the specified region
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    # Select the DynamoDB table named 'user'
    table = dynamodb.Table('User')

    # Get the email and name from the event
    email = event.get('Email', '').strip()  # Use strip to remove any leading/trailing whitespace
    name = event.get('Name', '').strip()  # Get the name to use as the sort key
    password = event.get('Password', '')

    try:
        # Get the item from DynamoDB using Email as the partition key and Name as the sort key
        response = table.get_item(Key={'Email': email, 'Name': name})

        # Check if the item exists
        if 'Item' in response:
            stored_username = response['Item'].get('Username')  # Ensure 'Username' is correctly capitalized
            stored_password = response['Item'].get('Password')  # Ensure 'Password' is correctly capitalized
            
            # Verify the password
            if password == stored_password:
                return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'Authentication successful', 'username': stored_username})
                }
            else:
                return {
                    'statusCode': 401,
                    'body': json.dumps({'message': 'Invalid credentials'})
                }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'User not found'})
            }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }