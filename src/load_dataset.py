import os
import pandas as pd

def load_unsw_nb15_data() -> pd.DataFrame:
    """
    Load the UNSW-NB15 training and testing datasets from the 'data' folder within the 'src' directory.

    Returns:
        pd.DataFrame: Combined dataset containing training and testing data.

    Raises:
        FileNotFoundError: If the dataset files are not found.
    """
    # Get the absolute path to the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "data")

    # File paths for the datasets
    train_file = os.path.join(data_dir, "UNSW_NB15_training-set.csv")
    test_file = os.path.join(data_dir, "UNSW_NB15_testing-set.csv")

    # Check if files exist
    if not os.path.exists(train_file):
        raise FileNotFoundError(f"Training dataset not found: {train_file}")
    if not os.path.exists(test_file):
        raise FileNotFoundError(f"Testing dataset not found: {test_file}")

    # Load datasets
    train_data = pd.read_csv(train_file)
    test_data = pd.read_csv(test_file)

    # Debugging outputs
    print(f"Training Data Loaded: {train_data.shape}")
    print(f"Testing Data Loaded: {test_data.shape}")

    # Combine datasets
    combined_data = pd.concat([train_data, test_data], ignore_index=True)
    print(f"Combined Data Loaded: {combined_data.shape}")

    return train_data, test_data, combined_data
