from lib.validators import validate_date, validate_int, validate_string, validate_float

def xml_to_db_insert_values(root, file_name):
    insert_values = []

    for transaction_tag in root.findall('transaction'):
        transaction_date = validate_date(input=transaction_tag.attrib['date'],file_name=file_name,file_type='XML',column_name='transaction_date')
        transaction_reseller_id = validate_int(input=transaction_tag.attrib['reseller-id'],file_name=file_name,file_type='XML',column_name='transaction_reseller_id')
        transaction_id = validate_int(input=transaction_tag.find('transactionId').text,file_name=file_name,file_type='XML',column_name='transaction_id')
        event_name = validate_string(input=transaction_tag.find('eventName').text,file_name=file_name,file_type='XML',column_name='event_name')
        number_of_purchased_tickets = validate_int(input=transaction_tag.find('numberOfPurchasedTickets').text,file_name=file_name,file_type='XML',column_name='number_of_purchased_tickets')
        total_amount = validate_float(input=transaction_tag.find('totalAmount').text,file_name=file_name,file_type='XML',column_name='total_amount')
        sales_channel = validate_string(input=transaction_tag.find('salesChannel').text,file_name=file_name,file_type='XML',column_name='sales_channel')
        customer = transaction_tag.find('customer')
        customer_first_name =  validate_string(input=customer.find('firstName').text,file_name=file_name,file_type='XML',column_name='customer_first_name')
        customer_last_Name = validate_string(input=customer.find('lastName').text,file_name=file_name,file_type='XML',column_name='customer_last_Name')
        office_location = validate_string(input=transaction_tag.find('officeLocation').text,file_name=file_name,file_type='XML',column_name='office_location')
        date_created = validate_date(input=transaction_tag.find('dateCreated').text,file_name=file_name,file_type='XML',column_name='date_created')
        
        insert_values.append((transaction_date, transaction_reseller_id,transaction_id,event_name,number_of_purchased_tickets, total_amount, sales_channel, customer_first_name, customer_last_Name, office_location, date_created))

    return insert_values