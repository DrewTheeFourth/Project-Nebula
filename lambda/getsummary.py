import json
import boto3
from decimal import Decimal

# Initialize DynamoDB resource and tables
dynamodb = boto3.resource('dynamodb')
summary_table = dynamodb.Table('Summary')
attendance_table = dynamodb.Table('Attendance')
assignment_table = dynamodb.Table('Assignment')
student_table = dynamodb.Table('Students')

def calculate_compliance(average, submitted):
    if average < 40:
        a_comp = "Low"
    elif average < 60:
        a_comp = "Medium"
    elif average < 80:
        a_comp = "Good"
    else:
        a_comp = "High"

    q_comp = (submitted * 100) / 18
    if q_comp < 40:
        q_comp = "Low"
    elif q_comp < 60:
        q_comp = "Medium"
    elif q_comp < 80:
        q_comp = "Good"
    else:
        q_comp = "High"

    score = (average * 70 + submitted * 30) / 100

    if score > 80:
        compliance = "High Compliance"
    elif score >= 60:
        compliance = "Good Compliance"
    elif score >= 30:
        compliance = "Medium Compliance"
    else:
        compliance = "Low Compliance"

    return a_comp, q_comp, score, compliance

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
        summary_items = []

        if email and name:
            # Query the Students table to retrieve specific student data
            student_response = student_table.get_item(
                Key={'Email': email, 'Name': name}
            )
            student_item = student_response.get('Item')

            if not student_item:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'message': 'Student not found.'})
                }

            # Retrieve Average from Attendance table
            attendance_response = attendance_table.get_item(
                Key={'Email': email, 'Name': name}
            )
            attendance_item = attendance_response.get('Item', {})
            average = Decimal(attendance_item.get('Average', 0))

            # Retrieve Submitted from Assignment table
            assignment_response = assignment_table.get_item(
                Key={'Email': email, 'Name': name}
            )
            assignment_item = assignment_response.get('Item', {})
            submitted = Decimal(assignment_item.get('Submitted', 0))

            # Calculate compliance values
            a_comp, q_comp, score, compliance = calculate_compliance(average, submitted)

            # Create summary item
            summary_item = {
                'Email': email,
                'Name': name,
                'Average': average,
                'Submitted': submitted,
                'A.Comp': a_comp,
                'Q.Comp': q_comp,
                'Score': score,
                'Compliance': compliance
            }

            # Add the item to the Summary table
            summary_table.put_item(Item=summary_item)
            summary_items.append(summary_item)

        else:
            # Scan the Students table to retrieve all student data
            students_response = student_table.scan()
            students = students_response['Items']

            for student in students:
                email = student['Email']
                name = student['Name']

                # Retrieve Average from Attendance table
                attendance_response = attendance_table.get_item(
                    Key={'Email': email, 'Name': name}
                )
                attendance_item = attendance_response.get('Item', {})
                average = Decimal(attendance_item.get('Average', 0))

                # Retrieve Submitted from Assignment table
                assignment_response = assignment_table.get_item(
                    Key={'Email': email, 'Name': name}
                )
                assignment_item = assignment_response.get('Item', {})
                submitted = Decimal(assignment_item.get('Submitted', 0))

                # Calculate compliance values
                a_comp, q_comp, score, compliance = calculate_compliance(average, submitted)

                # Create summary item
                summary_item = {
                    'Email': email,
                    'Name': name,
                    'Average': average,
                    'Submitted': submitted,
                    'A.Comp': a_comp,
                    'Q.Comp': q_comp,
                    'Score': score,
                    'Compliance': compliance
                }

                # Add the item to the Summary table
                summary_table.put_item(Item=summary_item)
                summary_items.append(summary_item)

        # Convert Decimal values to float for JSON serialization
        for item in summary_items:
            for key, value in item.items():
                if isinstance(value, Decimal):
                    item[key] = float(value)

        # Return the updated items
        return {
            'statusCode': 200,
            'body': json.dumps(summary_items, default=convert_decimals)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
