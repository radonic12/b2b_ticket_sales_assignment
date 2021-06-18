#sh ecs_deployment.sh
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 974280244436.dkr.ecr.us-east-2.amazonaws.com
docker build -t sales_information_spooler .
docker tag sales_information_spooler:latest 974280244436.dkr.ecr.us-east-2.amazonaws.com/sales_information_spooler:latest
docker push 974280244436.dkr.ecr.us-east-2.amazonaws.com/sales_information_spooler:latest