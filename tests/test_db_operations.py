import unittest
from database.db_operations import load_dataset, store_raw_data, store_preprocessed_data

class TestDatabaseOperations(unittest.TestCase):

    def test_load_dataset(self):
        query = "SELECT * FROM datasets WHERE id = %s"
        result = load_dataset(query, (1,))
        self.assertIsNotNone(result)  # Check if data was returned

    def test_store_raw_data(self):
        query = "INSERT INTO datasets (data_column1, data_column2) VALUES (%s, %s)"
        params = ('sample_data1', 'sample_data2')
        store_raw_data(query, params)

        # Verify that the data is inserted (you can perform a SELECT query to check)

    def test_store_preprocessed_data(self):
        query = "UPDATE preprocessed_data SET processed_column1 = %s WHERE dataset_id = %s"
        params = ('processed_data', 1)
        store_preprocessed_data(query, params)

        # Verify the update by selecting the updated data
        verify_query = "SELECT processed_column1 FROM preprocessed_data WHERE dataset_id = %s"
        result = load_dataset(verify_query, (1,))
        self.assertEqual(result[0][0], 'processed_data')  # Ensure the data was updated

if __name__ == "__main__":
    unittest.main()
