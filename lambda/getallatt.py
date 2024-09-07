import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Attendance')

def calculate_average(attendance_data):
    # Identify week items dynamically
    weeks = [key for key in attendance_data.keys() if key.startswith("week")]
    total = sum([attendance_data.get(week, 0) for week in weeks])
    
    # Calculate average only if there are weeks present
    average = total / len(weeks) if weeks else 0  # Avoid division by zero
    return average

def convert_decimals(obj):
    """Convert Decimal objects to floats for JSON serialization."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError("Type not serializable")

def lambda_handler(event, context):
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
            items = response['Items']

            if not items:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'message': 'Item not found.'})
                }

            # Calculate and update the average for the queried item
            for item in items:
                average = calculate_average(item)
                item['Average'] = average

                # Update the item in the DynamoDB table with the calculated average
                table.put_item(
                    Item={
                        'Email': item['Email'],  # Assuming Email is the primary key
                        'Name': item['Name'],  # Assuming Name is the sort key
                        'Average': average,
                        **{k: v for k, v in item.items() if k not in ['Average']}  # Exclude Average to avoid overwriting
                    }
                )

        else:
            # Scan the table to retrieve all items
            response = table.scan()
            items = response['Items']

            # Calculate and update the average for all items
            for item in items:
                average = calculate_average(item)
                item['Average'] = average

                # Update the item in the DynamoDB table with the calculated average
                table.put_item(
                    Item={
                        'Email': item['Email'],  # Assuming Email is the primary key
                        'Name': item['Name'],  # Assuming Name is the sort key
                        'Average': average,
                        **{k: v for k, v in item.items() if k not in ['Average']}  # Exclude Average to avoid overwriting
                    }
                )

        # Return the updated items
        return {
            'statusCode': 200,
            'body': json.dumps(items, default=convert_decimals)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
