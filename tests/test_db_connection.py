import unittest
from src.database.db_config import execute_query

class TestDatabaseConnection(unittest.TestCase):
    def test_connection(self):
        query = "SELECT * FROM test_table LIMIT 5;"
        result = execute_query(query)
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)

if __name__ == '__main__':
    unittest.main()
