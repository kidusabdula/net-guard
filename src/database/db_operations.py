import psycopg2
from .db_config import create_db_connection
import pandas as pd


def bulk_store_dataset(table_name, data_frame):
    connection = create_db_connection()
    cursor = connection.cursor()
    try:
        columns = ", ".join(data_frame.columns)
        values = ", ".join([f"%({col})s" for col in data_frame.columns])
        query = f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({values})
            ON CONFLICT (id) 
            DO UPDATE SET {', '.join([f"{col} = EXCLUDED.{col}" for col in data_frame.columns])};
        """
        data_dicts = data_frame.to_dict(orient="records")
        cursor.executemany(query, data_dicts)
        connection.commit()
        print(f"Data successfully stored in table: {table_name}")
    except Exception as e:
        print(f"Error storing data in {table_name}: {e}")
    finally:
        cursor.close()
        connection.close()


def fetch_table_data(table_name):
    try:
        connection = create_db_connection()
        
        query = f"SELECT * FROM {table_name};"
        data = pd.read_sql_query(query, connection)
        
        connection.close()  
        return data
    except Exception as e:
        print(f"Error fetching data from {table_name}: {e}")
        return None