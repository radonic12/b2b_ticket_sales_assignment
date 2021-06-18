import os
import psycopg2
from lib.aws import get_secret

def establish_connection(secret_name_value=None):
    secret_name = os.environ.get('aws_secret_name')
    if secret_name_value != None:
        secret_name = secret_name_value
    secret = get_secret(secret_name=secret_name)

    db_username = secret['username']
    db_password = secret['password']
    db_port = secret['port']
    db_name = secret['database']
    db_host = secret['host']

    conn = psycopg2.connect(database=db_name, user=db_username, password=db_password, host=db_host, port=db_port)
    cursor = conn.cursor()
    return conn, cursor

def db_insert(conn, cursor, insert_values):
    query= '''
    INSERT INTO sales_information 
        (
            transaction_date
            ,reseller_id
            ,transaction_id
            ,event_name
            ,number_of_purchased_tickets
            ,total_amount
            ,sales_channel
            ,customer_first_name
            ,customer_last_name
            ,office_location
            ,date_created
            ) 
        VALUES 
            (%s, %s, %s,%s, %s, %s,%s, %s, %s, %s, %s)
        on conflict(transaction_id) do update set 
            transaction_date=excluded.transaction_date
            ,reseller_id=excluded.reseller_id
            ,event_name=excluded.event_name
            ,number_of_purchased_tickets=excluded.number_of_purchased_tickets
            ,total_amount=excluded.total_amount
            ,sales_channel=excluded.sales_channel
            ,customer_first_name=excluded.customer_first_name
            ,customer_last_name=excluded.customer_last_name
            ,office_location=excluded.office_location
            ,date_created=excluded.date_created
            ,updated_at=excluded.updated_at'''
    cursor.executemany(query, insert_values)
    conn.commit()

def db_fetch(cursor, query):
    cursor.execute(query)
    
    return cursor.fetchall()

def db_execute(conn, cursor, query):
    cursor.execute(query)
    conn.commit()

def close_connection(conn, cursor):
    conn.close()
    cursor.close()
