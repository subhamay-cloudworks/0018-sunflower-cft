import boto3
import os
import csv
import logging
import json
import pandas as pd


# Load the exceptions for error handling
from botocore.exceptions import ClientError, ParamValidationError

s3_client = boto3.client('s3', region_name = os.environ.get('AWS_REGION'))
ses_client = boto3.client('ses',region_name=os.getenv('AWS_REGION'))

bucket_name = os.environ.get("S3_BUCKET_NAME")
sender = os.getenv('SENDER')
recipient= os.getenv('RECIPIENT')
configuration_set = os.getenv('CONFIGURATION_SET')
charset= os.getenv('CHARSET')
subject = os.getenv('SUBJECT')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def send_email_message(data_frame):

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                "This email was sent with Amazon SES using the "
                "AWS SDK for Python (Boto)."
                )
                
    # The HTML body of the email.
    BODY_HTML = f"""
    <html>
        <head></head>
        <body>
            <pre><{data_frame}</pre>
        </body>
    </html>
    """   

    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': charset,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': charset,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': charset,
                    'Data': subject,
                },
            },
            Source=sender#,
            # If you are not using a configuration set, comment or delete the
            # following line
            #ConfigurationSetName=configuration_set,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


def lambda_handler(event, context):
    try:
        logger.info(f"Hello from {context.function_name}")
        logger.info(f"event :: {json.dumps(event)}")
        for record in event["Records"]:
            if record["EventSource"] == "aws:sns" and record["Sns"]["Subject"] == "Amazon S3 Notification":
                s3_event = record["Sns"]["Message"]
                logger.info(f"type = {type(s3_event)}")
                logger.info(f's3_event = {s3_event}')
                message = json.loads(record['Sns']['Message'])
                for s3_event in message["Records"]:
                    logger.info(f"s3_event = {json.dumps(s3_event)}")
                    bucket_name = s3_event["s3"]["bucket"]["name"]
                    object_name = s3_event["s3"]["object"]["key"]
                    object_type = object_name.split(".")[-1]
                    if object_type in ["csv"]:
                        logger.info(f"S3 URI : s3://{bucket_name}/{object_name}")
                        response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
                        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

                        logger.info(f"Status = {status}") 
                        if status == 200:
                            logger.info(f"Successful S3 get_object response. Status - {status}")
                            df = pd.read_csv(response.get("Body"))
                            pd.set_option('display.max_columns', None)
                            pd.set_option('display.max_rows', None)
                            # logger.info(f"DataFrame shape : {df.shape}")
                            logger.info(df)
                            send_email_message(df)
                        else:
                            logger.error(f"Unsuccessful S3 get_object response. Status - {status}")


    except ParamValidationError as e:
        logger.error(f"Parameter validation error: {e}")
    except ClientError as e:
        logger.error(f"Client error: {e}")
        
    return "success"