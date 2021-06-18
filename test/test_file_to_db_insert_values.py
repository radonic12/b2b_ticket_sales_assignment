from datetime import datetime
import unittest
import xml.etree.ElementTree as ET
import unittest
import pandas as pd
from lib.parsers.csv_parser import csv_to_db_insert_values
from lib.parsers.xml_parser import xml_to_db_insert_values

class test_file_to_db_insert_values(unittest.TestCase):
    def test_csv_unwrap(self):
        file_name = 'testfile_01012021_123.csv'
        csv_data = pd.read_csv(f'test/data/csv/{file_name}', dtype={0:'str',1:'str',2:'str',3:'str',4:'str',5:'str',6:'str',7:'str',8:'str'})

        insert_values = csv_to_db_insert_values(file_name=file_name, csv_data=csv_data)
        
        desired_output_csv_to_db_insert_values = [(datetime.strptime('01012021', '%m%d%Y'), '123', '1', 'Event1', '12345', '100.00', 'office', 'Adam', 'Smith', 'Denmark', datetime.strptime('01022021', '%m%d%Y'))]
        self.assertEqual(insert_values, desired_output_csv_to_db_insert_values)

    def test_xml_unwrap(self):
        root = ET.parse('test/data/xml/test_file.xml').getroot()

        insert_values = xml_to_db_insert_values(root=root, file_name='test_file.xml')
        
        desired_xml_to_db_insert_values = [(datetime.strptime('01012021', '%m%d%Y'), '123', '1', 'Event1', '12345', '100.00', 'office', 'Adam', 'Smith', 'Denmark', datetime.strptime('01022021', '%m%d%Y'))]
        self.assertEqual(insert_values, desired_xml_to_db_insert_values)

    def test_csv_unwrap_bad_format(self):
        file_name = 'testfile_01012021_123.csv'
        csv_data = pd.read_csv(f'test/data/csv/{file_name}', dtype={0:'str',1:'str',2:'str',3:'str',4:'str',5:'str',6:'str',7:'str',8:'str'})
        
        column_name = 'Transaction ID'
        csv_data.at[0,column_name] = 'string'
        try:
            csv_to_db_insert_values(file_name=file_name, csv_data=csv_data)
            self.assertEqual(1, 2, f'wrongly formatted {column_name} did not fail properly')
        except Exception as e: 
            self.assertEqual(str(e).split('. Error thrown')[0],'input=string is not castable as int for file=testfile_01012021_123.csv of type=csv and column=transaction_id', f'wrong error thrown for wrongly formatted {column_name}')
        
        csv_data = pd.read_csv(f'test/data/csv/{file_name}', dtype={0:'str',1:'str',2:'str',3:'str',4:'str',5:'str',6:'str',7:'str',8:'str'})
        column_name = 'Number of purchased tickets'
        csv_data.at[0,column_name] = 'string'
        try:
            csv_to_db_insert_values(file_name=file_name, csv_data=csv_data)
            self.assertEqual(1, 2, f'wrongly formatted {column_name} did not fail properly')
        except Exception as e: 
            self.assertEqual(str(e).split('. Error thrown')[0],'input=string is not castable as int for file=testfile_01012021_123.csv of type=csv and column=number_of_purchased_tickets', f'wrong error thrown for wrongly formatted {column_name}')
        
        csv_data = pd.read_csv(f'test/data/csv/{file_name}', dtype={0:'str',1:'str',2:'str',3:'str',4:'str',5:'str',6:'str',7:'str',8:'str'})
        column_name = 'Total amount'
        csv_data.at[0,column_name] = 'string'
        try:
            csv_to_db_insert_values(file_name=file_name, csv_data=csv_data)
            self.assertEqual(1, 2, f'wrongly formatted {column_name} did not fail properly')
        except Exception as e: 
            self.assertEqual(str(e).split('. Error thrown')[0],'input=string is not castable as float for file=testfile_01012021_123.csv of type=csv and column=total_amount', f'wrong error thrown for wrongly formatted {column_name}')

        csv_data = pd.read_csv(f'test/data/csv/{file_name}', dtype={0:'str',1:'str',2:'str',3:'str',4:'str',5:'str',6:'str',7:'str',8:'str'})
        column_name = 'Created_Date'
        csv_data.at[0,column_name] = 'string'
        try:
            csv_to_db_insert_values(file_name=file_name, csv_data=csv_data)
            self.assertEqual(1, 2, f'wrongly formatted {column_name} did not fail properly')
        except Exception as e: 
            self.assertEqual(str(e).split('. Error thrown')[0],'input=string is not castable as date make sure the format is MMDDYYYY for file=testfile_01012021_123.csv of type=csv and column=date_created', f'wrong error thrown for wrongly formatted {column_name}')
    
    def test_xml_unwrap_bad_format(self):
        root = ET.parse('test/data/xml/test_file.xml').getroot()
        root.find('transaction').attrib['date'] = 'string'
        column_name = 'transaction.date'
        try:
            xml_to_db_insert_values(root=root, file_name='test_file.xml')
            self.assertEqual(1, 2, f'wrongly formatted {column_name} did not fail properly')
        except Exception as e: 
            self.assertEqual(str(e).split('. Error thrown')[0],'input=string is not castable as date make sure the format is MMDDYYYY for file=test_file.xml of type=XML and column=transaction_date', f'wrong error thrown for wrongly formatted {column_name}')
        
        root = ET.parse('test/data/xml/test_file.xml').getroot()
        root.find('transaction').attrib['reseller-id'] = 'string'
        column_name = 'transaction.reseller-id'
        try:
            xml_to_db_insert_values(root=root, file_name='test_file.xml')
            self.assertEqual(1, 2, f'wrongly formatted {column_name} did not fail properly')
        except Exception as e: 
            self.assertEqual(str(e).split('. Error thrown')[0],'input=string is not castable as int for file=test_file.xml of type=XML and column=transaction_reseller_id', f'wrong error thrown for wrongly formatted {column_name}')
        
        root = ET.parse('test/data/xml/test_file.xml').getroot()
        root.find('transaction').find('transactionId').text = 'string'
        column_name = 'transactionId'
        try:
            xml_to_db_insert_values(root=root, file_name='test_file.xml')
            self.assertEqual(1, 2, f'wrongly formatted {column_name} did not fail properly')
        except Exception as e: 
            self.assertEqual(str(e).split('. Error thrown')[0],'input=string is not castable as int for file=test_file.xml of type=XML and column=transaction_id', f'wrong error thrown for wrongly formatted {column_name}')
        
        root = ET.parse('test/data/xml/test_file.xml').getroot()
        root.find('transaction').find('numberOfPurchasedTickets').text = 'string'
        column_name = 'numberOfPurchasedTickets'
        try:
            xml_to_db_insert_values(root=root, file_name='test_file.xml')
            self.assertEqual(1, 2, f'wrongly formatted {column_name} did not fail properly')
        except Exception as e: 
            self.assertEqual(str(e).split('. Error thrown')[0],'input=string is not castable as int for file=test_file.xml of type=XML and column=number_of_purchased_tickets', f'wrong error thrown for wrongly formatted {column_name}')
        
        root = ET.parse('test/data/xml/test_file.xml').getroot()
        root.find('transaction').find('totalAmount').text = 'string'
        column_name = 'totalAmount'
        try:
            xml_to_db_insert_values(root=root, file_name='test_file.xml')
            self.assertEqual(1, 2, f'wrongly formatted {column_name} did not fail properly')
        except Exception as e: 
            self.assertEqual(str(e).split('. Error thrown')[0],'input=string is not castable as float for file=test_file.xml of type=XML and column=total_amount', f'wrong error thrown for wrongly formatted {column_name}')

        root = ET.parse('test/data/xml/test_file.xml').getroot()
        root.find('transaction').find('dateCreated').text = 'string'
        column_name = 'dateCreated'
        try:
            xml_to_db_insert_values(root=root, file_name='test_file.xml')
            self.assertEqual(1, 2, f'wrongly formatted {column_name} did not fail properly')
        except Exception as e: 
            self.assertEqual(str(e).split('. Error thrown')[0],'input=string is not castable as date make sure the format is MMDDYYYY for file=test_file.xml of type=XML and column=date_created', f'wrong error thrown for wrongly formatted {column_name}')

