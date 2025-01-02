import os
import pandas as pd
from pathlib import Path

def raw_dataset_loader(train_file_path=None, test_file_path=None):
 
    if train_file_path is None or test_file_path is None:
        base_path = Path(__file__).parent.parent.parent / 'data'
        train_file_path = base_path / 'UNSW_NB15_training_set.csv'
        test_file_path = base_path / 'UNSW_NB15_testing_set.csv'
    
    print("Checking file paths...")
    print(f"Train file path: {train_file_path}")
    print(f"Test file path: {test_file_path}")
    
    if not os.path.exists(train_file_path):
        print(f"Train file not found at {train_file_path}. Please check the path.")
        return None, None, None
    if not os.path.exists(test_file_path):
        print(f"Test file not found at {test_file_path}. Please check the path.")
        return None, None, None
    
    try:
        train_df = pd.read_csv(train_file_path)
        test_df = pd.read_csv(test_file_path)
        
        combined_df = pd.concat([train_df, test_df], ignore_index=True)
        print("Datasets loaded and combined successfully.")
        return train_df, test_df, combined_df
    
    except Exception as e:
        print(f"Error loading datasets: {str(e)}")
        return None, None, None
