import boto3
from datetime import datetime
import io
import os 
import pandas as pd
import xml.etree.ElementTree as et
from lib.aws import s3_move_file, s3_delete_single_file
from lib.db import establish_connection,close_connection,db_insert
from lib.parsers.xml_parser import xml_to_db_insert_values
from lib.parsers.csv_parser import csv_to_db_insert_values

def spooler():
    bucket_name = os.environ.get('aws_s3_bucket_name')
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(f'{bucket_name}')
    prefix = 'unprocessed/'
    
    conn, cursor = establish_connection()

    for my_bucket_object in bucket.objects.filter(Prefix=prefix):
        key = my_bucket_object.key
        if key == prefix:
            continue
        
        print(f'Spooling of {key} started at {datetime.now()}')
        
        file_extension = key.split('.')[-1]
        file_body = my_bucket_object.get()['Body'].read()
        file_name = key.split('/')[-1]
        
        insert_values = None

        if file_extension == 'xml':
            root = et.fromstring(file_body)
            insert_values = xml_to_db_insert_values(root=root,file_name=key)
        elif file_extension == 'csv':
            csv_data = pd.read_csv(io.BytesIO(file_body))#,header=None, encoding='utf8',sep=',')
            insert_values = csv_to_db_insert_values(file_name=key, csv_data=csv_data)
        else: 
            print(f'Unkown filetype={file_extension} parsed to spooler through bucket={bucket_name} and key={key}. Error thrown at {datetime.now()}')
            continue
        
        db_insert(conn=conn, cursor=cursor, insert_values=insert_values)
        s3_move_file(bucket_name=bucket_name, key=file_name)
        s3_delete_single_file(key=key)
        
        print(f'Spooling of {key} ended at {datetime.now()}')
    
    close_connection(conn=conn, cursor=cursor)