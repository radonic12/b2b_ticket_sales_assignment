import os

def set_environment_variables():
    environment = os.environ.get('environment')

    if environment == 'live':
        os.environ['aws_secret_name'] = 'db_credentials'
        os.environ['aws_s3_bucket_name'] = 'files-containing-sales-information'
    else:
        os.environ['aws_secret_name'] = 'test_db_credentials'
        os.environ['aws_s3_bucket_name'] = 'files-containing-sales-information-test'