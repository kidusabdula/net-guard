import os
import pandas as pd
from pathlib import Path

class DataLoaderFactory:
    def __init__(self, file_path=None):
        self.file_path = file_path

    def load_raw_data(self, train_file_path=None, test_file_path=None):
        if train_file_path is None or test_file_path is None:
            base_path = Path(__file__).parent.parent.parent / 'data'
            train_file_path = base_path / 'UNSW_NB15_training_set.csv'
            test_file_path = base_path / 'UNSW_NB15_testing_set.csv'
    
        if not os.path.exists(train_file_path):
            raise FileNotFoundError(f"Train file not found at {train_file_path}")
        if not os.path.exists(test_file_path):
            raise FileNotFoundError(f"Test file not found at {test_file_path}")
    
        try:
            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)
            combined_df = pd.concat([train_df, test_df], ignore_index=True)
            
            return train_df, test_df, combined_df
    
        except Exception as e:
            raise Exception(f"Error loading datasets: {str(e)}")
