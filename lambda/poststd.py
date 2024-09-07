import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Initialize a DynamoDB resource object for the specified region
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    # Select the DynamoDB table named 'Students'
    table = dynamodb.Table('Students')  # Ensure the table name matches exactly

    # Extract values from the event object
    email = event.get('Email')
    name = event.get('Name')
    cohort = event.get('Cohort')
    sex = event.get('Sex')
    nationality = event.get('Nationality')

    # Validate input
    if not email or not name or not cohort or not sex or not nationality:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'All fields (Email, Name, Cohort, Sex, Nationality) are required.'})
        }

    try:
        # Add the item to the DynamoDB table
        response = table.put_item(
            Item={
                'Email': email,
                'Name': name,
                'Cohort': cohort,
                'Sex': sex,
                'Nationality': nationality
            }
        )

        # Return a success message
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Item added successfully!', 'response': response})
        }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }