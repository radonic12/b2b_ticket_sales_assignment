from lib.validators import validate_date, validate_int, validate_string, validate_float

def csv_to_db_insert_values(file_name, csv_data):
    file_name_split = file_name.split('.')
    file_name_split = file_name_split[0].split('_')

    transaction_date = validate_date(input=file_name_split[1], file_name=file_name,file_type='csv', column_name='transaction_date')
    transaction_reseller_id = validate_int(input=file_name_split[2], file_name=file_name,file_type='csv', column_name='transaction_reseller_id')

    insert_values = []

    for _, row in csv_data.iterrows():    
        transaction_id = validate_int(input=row['Transaction ID'], file_name=file_name,file_type='csv', column_name='transaction_id')
        event_name = validate_string(input=row['Event name'], file_name=file_name,file_type='csv', column_name='event_name')
        number_of_purchased_tickets = validate_int(input=row['Number of purchased tickets'], file_name=file_name,file_type='csv', column_name='number_of_purchased_tickets')
        total_amount = validate_float(input=row['Total amount'], file_name=file_name,file_type='csv', column_name='total_amount')
        sales_channel = validate_string(input=row['Sales channel'], file_name=file_name,file_type='csv', column_name='sales_channel')
        customer_first_name = validate_string(input=row['Customer first name'], file_name=file_name,file_type='csv', column_name='customer_first_name')
        customer_last_name = validate_string(input=row['Customer last name'], file_name=file_name,file_type='csv', column_name='customer_last_name')
        office_location = validate_string(input=row['Office location'], file_name=file_name,file_type='csv', column_name='office_location')
        date_created = validate_date(input=row['Created_Date'], file_name=file_name,file_type='csv', column_name='date_created')
        
        insert_values.append((transaction_date, transaction_reseller_id,transaction_id,event_name,number_of_purchased_tickets, total_amount, sales_channel, customer_first_name, customer_last_name, office_location, date_created))
    
    return insert_values