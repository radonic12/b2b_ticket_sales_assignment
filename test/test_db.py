import unittest
from lib.db import establish_connection, close_connection, db_insert, db_fetch, db_execute
from lib.enviroment_variables import set_environment_variables

class test_db(unittest.TestCase):
    def test_db_connection(self):
        set_environment_variables()
        conn, cursor = establish_connection()
        close_connection(conn=conn,cursor=cursor)
        #No errors thrown will be the success criteria

    def test_db_inserts(self):
        set_environment_variables()
        
        conn, cursor = establish_connection()
        
        query = f'delete from sales_information where transaction_id=1'
        db_execute(conn=conn, cursor=cursor, query=query)

        insert_values = [('2021-01-01', '123', '1', 'Event1', '12345', '100.00', 'office', 'Adam', 'Smith', 'Denmark', '2021-01-02')]
        db_insert(conn=conn, cursor=cursor,insert_values=insert_values)

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

        self.assertEqual(insert_values,actual_values)

    def test_duplicate_db_inserts(self):
        set_environment_variables()
        
        conn, cursor = establish_connection()
        
        query = f'delete from sales_information where transaction_id=1'
        db_execute(conn=conn, cursor=cursor, query=query)

        insert_values = [('2021-01-01', '123', '1', 'Event1', '12345', '100.00', 'office', 'Adam', 'Smith', 'Denmark', '2021-01-02')]
        db_insert(conn=conn, cursor=cursor,insert_values=insert_values)
        db_insert(conn=conn, cursor=cursor,insert_values=insert_values)

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

        self.assertEqual(insert_values,actual_values)

    def test_duplicate_db_upserts(self):
        set_environment_variables()
        
        conn, cursor = establish_connection()
        
        query = f'delete from sales_information where transaction_id=1'
        db_execute(conn=conn, cursor=cursor, query=query)

        insert_values = [('2021-01-01', '123', '1', 'Event1', '12345', '100.00', 'office', 'Adam', 'Smith', 'Denmark', '2021-01-02')]
        db_insert(conn=conn, cursor=cursor,insert_values=insert_values)
        query = 'select updated_at from sales_information where transaction_id=1'
        updated_at_insert = db_fetch(cursor=cursor,query=query)

        insert_values = [('2021-03-01', '1234', '1', 'Event2', '1234', '99.00', 'web', 'Jimmy', 'Smithen', 'USA', '2021-02-02')]
        db_insert(conn=conn, cursor=cursor,insert_values=insert_values)
        query = 'select updated_at from sales_information where transaction_id=1'
        updated_at_upsert = db_fetch(cursor=cursor,query=query)

        self.assertNotEqual(updated_at_insert,updated_at_upsert,'updated_at is not being updated')

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

        self.assertEqual(insert_values,actual_values)