import os
import unittest
from lib.aws import s3_delete_all_files_in_bucket, s3_upload, s3_count_files
from lib.db import establish_connection, close_connection, db_insert, db_fetch, db_execute
from lib.enviroment_variables import set_environment_variables
from lib.spooler import spooler

class test_spooler(unittest.TestCase):
    def test_spooling_xml(self):
        set_environment_variables()
        conn, cursor = establish_connection()

        s3_delete_all_files_in_bucket(prefix = 'unprocessed/')
        s3_delete_all_files_in_bucket(prefix = 'processed/')
        s3_upload(filename='test_file.xml', local_path='test/data/xml/test_file.xml', s3_folder='unprocessed/')
        
        spooler()
        
        query = f'''
        select 
            transaction_date::text
            ,reseller_id::text
            ,transaction_id::text
            ,event_name::text
            ,number_of_purchased_tickets::text
            ,total_amount::text
            ,sales_channel::text
            ,customer_first_name::text
            ,customer_last_name::text
            ,office_location::text
            ,date_created::text
        from sales_information 
            where transaction_id=1
        '''
        actual_values = db_fetch(cursor=cursor,query=query)

        close_connection(conn=conn, cursor=cursor)
        desired_values = [('2021-01-01', '123', '1', 'Event1', '12345', '100.00', 'office', 'Adam', 'Smith', 'Denmark', '2021-01-02')]
        
        self.assertEqual(desired_values,actual_values, 'values not inserted correctly in db')

        file_count = s3_count_files(prefix='unprocessed/')
        self.assertEqual(file_count,0,'files were not deleted from the unprocessed/ folder')

        file_count = s3_count_files(prefix='processed/')
        self.assertEqual(file_count,1,'files were not transfered to the processed/ folder')

    def test_spooling_csv(self):
        set_environment_variables()
        conn, cursor = establish_connection()

        s3_delete_all_files_in_bucket(prefix = 'unprocessed/')
        s3_delete_all_files_in_bucket(prefix = 'processed/')
        s3_upload(filename='testfile_01012021_123.csv', local_path='test/data/csv/testfile_01012021_123.csv', s3_folder='unprocessed/')
        
        spooler()
        
        query = f'''
        select 
            transaction_date::text
            ,reseller_id::text
            ,transaction_id::text
            ,event_name::text
            ,number_of_purchased_tickets::text
            ,total_amount::text
            ,sales_channel::text
            ,customer_first_name::text
            ,customer_last_name::text
            ,office_location::text
            ,date_created::text
        from sales_information 
            where transaction_id=1
        '''
        actual_values = db_fetch(cursor=cursor,query=query)

        close_connection(conn=conn, cursor=cursor)
        desired_values = [('2021-01-01', '123', '1', 'Event1', '12345', '100.00', 'office', 'Adam', 'Smith', 'Denmark', '2021-01-02')]
        
        self.assertEqual(desired_values,actual_values,'values not inserted correctly in db')

        file_count = s3_count_files(prefix='unprocessed/')
        self.assertEqual(file_count,0,'files were not deleted from the unprocessed/ folder')

        file_count = s3_count_files(prefix='processed/')
        self.assertEqual(file_count,1,'files were not transfered to the processed/ folder')