import boto3
import json
import os

def get_secret(secret_name):
    region_name = 'us-east-2'

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
   
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )

    secret = get_secret_value_response['SecretString']
    secret = json.loads(secret)  
      
    return secret

def s3_upload(filename, local_path, s3_folder):
    s3 = boto3.resource('s3')
    bucket_name = os.environ.get('aws_s3_bucket_name')
    s3.meta.client.upload_file(local_path, bucket_name, f'{s3_folder}{filename}')

def s3_delete_all_files_in_bucket(prefix):
    bucket_name = os.environ.get('aws_s3_bucket_name')
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(f'{bucket_name}')

    for my_bucket_object in bucket.objects.filter(Prefix=prefix):
        key = my_bucket_object.key
        if key == prefix:
            continue
        s3.Object(bucket_name, key).delete()

def s3_move_file(bucket_name, key):
    s3 = boto3.resource('s3')
    copy_source = {
        'Bucket': bucket_name,
        'Key': f'unprocessed/{key}'
    }
    s3.meta.client.copy(copy_source, bucket_name, f'processed/{key}')

def s3_delete_single_file(key):
    bucket_name = os.environ.get('aws_s3_bucket_name')
    s3 = boto3.resource('s3')
    s3.Object(bucket_name, key).delete()

def s3_count_files(prefix):
    bucket_name = os.environ.get('aws_s3_bucket_name')
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(f'{bucket_name}')

    counter = 0

    for my_bucket_object in bucket.objects.filter(Prefix=prefix):
        key = my_bucket_object.key
        if key == prefix:
            continue
        counter += 1
    
    return counter
