import json
import boto3
from decimal import Decimal, InvalidOperation

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Assignment')

def lambda_handler(event, context):
    # Extract values from the event object
    email = event.get('Email')
    name = event.get('Name')
    week1 = event.get('week1')
    week2 = event.get('week2')
    week3 = event.get('week3')
    week4 = event.get('week4')
    week5 = event.get('week5')

    # Validate required fields
    if not email or not name:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Email and Name are required.'})
        }

    # Create the item to put into the Assignments table
    try:
        item = {
            'Email': email,
            'Name': name,
            'week1': Decimal(str(week1)) if week1 is not None else Decimal(0),
            'week2': Decimal(str(week2)) if week2 is not None else Decimal(0),
            'week3': Decimal(str(week3)) if week3 is not None else Decimal(0),
            'week4': Decimal(str(week4)) if week4 is not None else Decimal(0),
            'week5': Decimal(str(week5)) if week5 is not None else Decimal(0),
        }
    except (InvalidOperation, ValueError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'Invalid week value: {str(e)}'})
        }

    try:
        # Put the item into the DynamoDB table
        table.put_item(Item=item)

        # Convert Decimals to floats before returning in the response
        for key in item:
            if isinstance(item[key], Decimal):
                item[key] = float(item[key])

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Item added successfully!', 'item': item})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }