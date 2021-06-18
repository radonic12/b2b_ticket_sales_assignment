CREATE TYPE valid_sales_channels AS ENUM ('office', 'web', 'mobile app');

create table sales_information (
    id SERIAL PRIMARY KEY,
    transaction_id BIGINT not null unique,
    transaction_date date,
    reseller_id int,
    event_name TEXT,
    number_of_purchased_tickets INT,
    total_amount NUMERIC(20,2),
    sales_channel valid_sales_channels,
    customer_first_name text,
    customer_last_name text,
    office_location text,
    date_created Date,
    created_at timestamp DEFAULT now(),
    updated_at timestamp DEFAULT now()

)

create table cache_system (
    id SERIAL PRIMARY KEY,
    database_name text,
    table_name text,
    last_updated_at timestamp,
    created_at timestamp DEFAULT now(),
    updated_at timestamp DEFAULT now()
)