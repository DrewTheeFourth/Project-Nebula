import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Assignment')

def calculate_submitted_and_acomp(assignments_data):
    # Identify week items dynamically
    weeks = [key for key in assignments_data.keys() if key.startswith("week")]
    submitted = sum([assignments_data.get(week, Decimal(0)) for week in weeks])
    a_comp = sum([1 for week in weeks if assignments_data.get(week, Decimal(0)) > Decimal(0)])
    return submitted, a_comp

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

            # Calculate and update the submitted and a_comp for the queried item
            for item in items:
                submitted, a_comp = calculate_submitted_and_acomp(item)
                item['Submitted'] = submitted
                item['A.Comp'] = a_comp

                # Update the item in the DynamoDB table with the calculated values
                table.put_item(
                    Item={
                        'Email': item['Email'],  # Assuming Email is the primary key
                        'Name': item['Name'],    # Assuming Name is the sort key
                        'Submitted': submitted,
                        'A.Comp': a_comp,
                        **{k: v for k, v in item.items() if k not in ['Submitted', 'A.Comp']}  # Include other fields from the item
                    }
                )

        else:
            # Scan the table to retrieve all items
            response = table.scan()
            items = response['Items']

            # Calculate and update the submitted and a_comp for all items
            for item in items:
                submitted, a_comp = calculate_submitted_and_acomp(item)
                item['Submitted'] = submitted
                item['A.Comp'] = a_comp

                # Update the item in the DynamoDB table with the calculated values
                table.put_item(
                    Item={
                        'Email': item['Email'],  # Assuming Email is the primary key
                        'Name': item['Name'],    # Assuming Name is the sort key
                        'Submitted': submitted,
                        'A.Comp': a_comp,
                        **{k: v for k, v in item.items() if k not in ['Submitted', 'A.Comp']}  # Include other fields from the item
                    }
                )

        # Convert Decimal values to float for JSON serialization
        for item in items:
            for key, value in item.items():
                if isinstance(value, Decimal):
                    item[key] = float(value)

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
