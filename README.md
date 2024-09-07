1. Create an S3 Bucket to Host Your Static Website
    Login to AWS Management Console.
     Go to S3.
    Click on Create bucket.
    Provide a unique Bucket name.
    Uncheck the Block all public access option, as we need the website to be publicly accessible.
    Click Create bucket.

    After creating the bucket, go to the Permissions tab and update the Bucket Policy to allow public read access:

        {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}

Enable static website hosting:

    Go to the Properties tab.
    Scroll down to the Static website hosting section and enable it.
    Set the index document (e.g., index.html).

Upload the website files (HTML, CSS, JS) to the S3 bucket.

2. Create Lambda Functions
    Navigate to AWS Lambda.
    Click Create Function.
    Choose Author from Scratch, provide a name (e.g., GetStudents, AddStudent), and set Runtime to Python 3.x (or any language you prefer).
    In the function code, add the necessary logic for interacting with DynamoDB.
    Save and deploy the functions.

3. Set Up API Gateway
    Login to AWS Management Console.
    Navigate to API Gateway.
    Choose Create API and select REST API.
    Define routes for your API:
    Example routes:
        GET /students (Retrieve all students)
        POST /student (Add a new student)
    Set up integration with Lambda functions. Link the Lambda functions to API Gateway by adding them to the respective routes created earlier.
    Deploy the API and note the API Endpoint URL, which will be used in the static website to send requests.

4. Set Up DynamoDB
    Navigate to DynamoDB in the AWS Console.
    Click Create Table.
    Name your table (e.g., Students).
    Define the primary key as:
    Partition key: Email (String)
    Sort key (optional): Name (String)
    Create the table and note the table name.

5. Update the Static Website with API Endpoints
    In your static website (JavaScript), update the API_ENDPOINT variable with the correct API Gateway URL.
    Ensure your JavaScript makes requests to the API Gateway.
