from lib.aws import get_secret
from lib.db import establish_connection, close_connection, db_fetch, db_insert, db_execute

def cache_updated_query(database_name, table_name, last_updated_at):

    return f'insert into cache_system (database_name, table_name, last_updated_at) VALUES ({database_name}, {table_name}, {last_updated_at})'

def cache_external_db():
    internal_conn, internal_cursor = establish_connection()

    query = '''
        select 
            database_name
            , table_name
            , max(last_updated_at) as last_updated
        from cache_system
        group by 1, 2
        '''

    external_databases = db_fetch(cursor=internal_cursor,query=query)

    for ex_db in external_databases:
        database_name = ex_db['database_name']
        table_name = ex_db['table_name']
        last_updated = ex_db['last_updated']
        external_conn, external_cursor = establish_connection(secret_name_value=database_name)

        query = f'select * from {table_name} where updated_at >= {last_updated} order by updated_at asc'
        external_rows = db_fetch(cursor=external_cursor,query=query)

        for row in external_rows:
            new_updated_at = row['updated_at']
            db_insert(conn=external_conn,cursor=external_cursor,insert_values=row)
            query = cache_updated_query(database_name=database_name,table_name=table_name,last_updated_at=new_updated_at)
            db_execute(conn=external_conn,cursor=external_cursor,query=query)
        close_connection(conn=external_conn,cursor=external_cursor)
    
    close_connection(conn=internal_conn,cursor=internal_cursor)
