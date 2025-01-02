import pandas as pd
import psycopg2
from src.database.db_operations import bulk_store_dataset
from src.database.db_config import create_db_connection
from preprocessing.raw_dataset_loader import raw_dataset_loader

# Load test DataFrame
train_df, test_df, combined_df = raw_dataset_loader()
mock_df = test_df

# Test function
def test_bulk_store_dataset():
    # Connection setup
    connection = create_db_connection()
    cursor = connection.cursor()

    try:

        # Call the function to store data
        bulk_store_dataset("unsw_nb15_test_table", mock_df)

        # Verify the data
        cursor.execute("SELECT feature1, feature2, feature3 FROM unsw_nb15_test_table;")
        rows = cursor.fetchall()

        # Convert fetched rows to a DataFrame
        fetched_df = pd.DataFrame(rows, columns=["feature1", "feature2", "feature3"])

        # Assert equality between the input and fetched DataFrames
        pd.testing.assert_frame_equal(mock_df.reset_index(drop=True), fetched_df.reset_index(drop=True))
        
        print("Test passed: Data stored and verified successfully!")

    except Exception as e:
        print(f"Test failed: {e}")
    finally:
        # Clean up: Drop the test table
        cursor.execute("DROP TABLE IF EXISTS unsw_nb15_test_table;")
        connection.commit()

        cursor.close()
        connection.close()

# Run the test
if __name__ == "__main__":
    test_bulk_store_dataset()
