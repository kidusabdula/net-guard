import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv
load_dotenv() 


def load_db_credentials():
    db_credentials = {
        'host': os.getenv('DB_HOST', 'localhost'),  
        'port': int(os.getenv('DB_PORT', '5432')),      
        'dbname': os.getenv('DB_NAME', 'net_guard'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', '1015')  
    }
    
    if not db_credentials['password']:
        raise ValueError("Database password is required")

    return db_credentials
    

def create_db_connection():
    credentials = load_db_credentials()
    try:
        connection = psycopg2.connect(
            host=credentials['host'],
            port=credentials['port'],
            dbname=credentials['dbname'],
            user=credentials['user'],
            password=credentials['password']
        )
        print("Database connection successful")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def close_db_connection(connection):
    if connection:
        connection.close()
        print("Database connection closed")

def execute_query(query, params=None):
    connection = create_db_connection()
    if connection is None:
        return None

    with connection.cursor() as cursor:
        try:
            cursor.execute(query, params)
            if query.strip().lower().startswith('select'):
                return cursor.fetchall()  
            connection.commit()
            print("Query executed successfully")
        except Exception as e:
            print(f"Error executing query: {e}")
        finally:
            close_db_connection(connection)
