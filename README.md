# b2b_ticket_sales_assignment
## Architecture
### Quick overview
A visual representation of Architecture can be found [here](https://www.dropbox.com/s/w1cd1m3ln6fojr2/achitecture.jpg?dl=0)

S3-bucket can be found [here](https://s3.console.aws.amazon.com/s3/buckets/files-containing-sales-information?region=us-east-2&tab=objects)
The ECS-cluster and task can be hound [here](https://us-east-2.console.aws.amazon.com/ecs/home?region=us-east-2#/clusters/ECL/services)
The ECR repo holding the python task can be found [here](https://us-east-2.console.aws.amazon.com/ecr/repositories/private/974280244436/sales_information_spooler?region=us-east-2)
The BI-database can be found [here](https://us-east-2.console.aws.amazon.com/rds/home?region=us-east-2#database:id=project-database;is-cluster=false)
### Deeper dive
DB-credentials are stored in [AWS secret manager](https://us-east-2.console.aws.amazon.com/secretsmanager/home?region=us-east-2#!/listSecrets)
When a file is uploaded to the S3 the ECS-task containing the Python spooler is started. This is setup using the following [tutorial](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/CloudWatch-Events-tutorial-ECS.html)

## Setup code to run locally
If you have difficulties installing psyciog2 run "brew install postgresql” 

To be able to use AWS boto3 sdk you need to [Install aws cli] (https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Configure aws cli] (https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)

Then you to add a setup.py file containing the following code:
```
curl -sL "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
python -m zipfile -e awscli-bundle.zip .
chmod +x ./awscli-bundle/install
./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws
aws configure set aws_access_key_id {}
aws configure set aws_secret_access_key {}
aws configure set default.region us-east-2
aws configure set default.output json
```
Make sure the aws_access_key_id and aws_secret_access_key are from an IAM user with proper permissions aws account id 974280244436

