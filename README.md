# Project Sunflower: Accessing a S3 bucket in one AWS Account (Account-A) from a Lambda function in another AWS Account(Account-B).


## Description

This sample project demonstrate how to access an objects in a S3 bucket in one Account from another. A S3 Bucket is created in Account-A. A SNS Topic is setup for event notification once a file is uploaded to the bucket. A Lambda function is created in Account-B and created a subscription to the SNS Topic. Once a file is uploaded to the bucket, S3 event notification send an event to SNS Topic and the Lambda function is triggered. The Lambda, in Account-B reads the file from the S3 bucket using bucket policy and uses Python Pandas to render it as a dataframe and sends an an email using AWS SES.The entire stack is created AWS CloudFormation.

![Project Sunflower - Design Diagram](https://subhamay-projects-repository-us-east-1.s3.amazonaws.com/0018-sunflower/sunflower-architecture-diagram.png?)

![Project Sunflower - Services Used](https://subhamay-projects-repository-us-east-1.s3.amazonaws.com/0018-sunflower/sunflower-services-used.png?)


### Dependencies

* You need to have two AWS Accounts to implement this.
* Create three Customer Managed KMS Keys in the regions where you want to create the stack. First two in Account-A and the third one in Account-B
* Modify the KMS Key Policy to let the AWS Account (root) encrypt / decrypt using any resource using the created KMS Key. In the destination account KMS Key policy, grant permission to source account to use the key for S3 bucket.

### Installing

* Clone the repository.
* Create a S3 bucket as code repository to store the CF templates.
* Create the folders - sunflower/cft
* Upload the following YAML template to sunflower/cft/
    * sunflower-stack-set.yaml
* Upload the following YAML template to sunflower/nested-stacks/
    * s3-stack.yaml
    * sns-stack
* Modify the following YAML template and provide the sender and receiver email address and setup them in AWS SES identity and upload the  
    same to sunflower/stack-set-templates/
    * lambda-function-stack.yaml
*  Zip and upload the following python lambda code to sunflower/code/python/
    *  lambda_function.zip
*  Setup AWS CloudFormation Stack Set Administration Role and AWS CloudFormation Stack Set Execution Role in Account-A.
    * Log in to Account-A
    * Create CloudFormation Stack Set Administration Role in both the source and destination accounts using the CF Template https://s3.amazonaws.com/cloudformation-stackset-sample-templates-us-east-1/AWSCloudFormationStackSetAdministrationRole.yml
    * Create CloudFormation Stack Set Execution Role in both the source and destination accounts using the CF Template https://s3.amazonaws.com/cloudformation-stackset-sample-templates-us-east-1/AWSCloudFormationStackSetExecutionRole.yml. Pass the Administration Account Id (the Account Id of Account -A)
*  Setup AWS CloudFormation Stack Set Administration Role and AWS CloudFormation Stack Set Execution Role in Account-B.
    * Log in to Account-B
    * Create CloudFormation Stack Set Administration Role in both the source and destination accounts using the CF Template https://s3.amazonaws.com/cloudformation-stackset-sample-templates-us-east-1/AWSCloudFormationStackSetAdministrationRole.yml
    * Create CloudFormation Stack Set Execution Role in both the source and destination accounts using the CF Template https://s3.amazonaws.com/cloudformation-stackset-sample-templates-us-east-1/AWSCloudFormationStackSetExecutionRole.yml. Pass the Administration Account Id (the Account Id of Account -A)
* Create the entire stack using CloudFormation StackSet from AWS Account A with the template sunflower-stack-set.yaml


### Executing program

* Upload the sample sample csv to the S3 bucket in Account-A
* Within a few seconds (depending on the size) the csv file will be read using Python Pandas and an email will be sent to the reciepient address

## Help

Post message in my blog (https://blog.subhamay.com)


## Authors

Contributors names and contact info

Subhamay Bhattacharyya  - [subhamay.aws@gmail.com](https://blog.subhamay.com)

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under Subhamay Bhattacharyya. All Rights Reserved.

## Acknowledgments

Inspiration, code snippets, etc.
* [Stephane Maarek ](https://www.linkedin.com/in/stephanemaarek/)
* [Neal Davis](https://www.linkedin.com/in/nealkdavis/)
* [Adrian Cantrill](https://www.linkedin.com/in/adriancantrill/)
