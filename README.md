Gold Grid User Management System
Overview
The Gold Grid User Management System is designed to streamline user management by providing functionalities for adding new users, sending notifications, and displaying real-time data. This solution utilizes AWS Lambda, API Gateway, SNS, and DynamoDB to create a seamless and automated user management process.

Features
Add New Users:

Collect user data via forms, including:
Full Name
Age
Occupation
Nationality
Marital Status
Email Address
Store the collected data in an AWS DynamoDB table.
Add Notification:

Send an email confirmation upon form submission using AWS SNS.
The confirmation email includes a personalized message, e.g., "Thank you for filling out the form. Welcome to the Gold Grid family."
Dashboard:

Display real-time data, including:
Users logged onto the app
Total number of users
Timestamp of user logins
Nationality distribution of users
Automation:

Implement automated processes to reduce manual intervention and allow the Gold Grid team to focus on other projects.
Architecture
AWS Lambda: Handles backend logic for processing user data and interacting with other AWS services.
API Gateway: Provides a RESTful API endpoint for user data submission.
AWS SNS: Manages email notifications for user confirmations.
DynamoDB: Stores user data and supports real-time data retrieval for the dashboard.
Setup
AWS Lambda:

Create a Lambda function for handling user data and notifications.
Set up appropriate IAM roles and policies for Lambda execution.
API Gateway:

Configure API Gateway to trigger the Lambda function upon receiving user data submissions.
Define the API endpoints and request/response mappings.
AWS SNS:

Create an SNS topic for sending email notifications.
Configure Lambda to publish messages to the SNS topic.
DynamoDB:

Set up a DynamoDB table with appropriate schema to store user data.
Configure Lambda to write user data to the DynamoDB table.
Usage
Adding New Users:

Access the form provided by the API Gateway.
Fill out the form with user information and submit it.
The data is processed by Lambda and stored in DynamoDB.
Receiving Notifications:

Upon form submission, an email confirmation is sent via SNS to the provided email address.
Viewing the Dashboard:

Access the dashboard to view real-time metrics and user data.
The dashboard displays information on logged-in users, total user count, login timestamps, and nationality distribution.
Contributing
Contributions are welcome! Please fork the repository and submit pull requests for any enhancements or bug fixes.
For any questions or issues, open an issue in the GitHub repository.

