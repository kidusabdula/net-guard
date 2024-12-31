import pandas as pd
import os

def load_data(file_path):
    """
    Loads the preprocessed dataset from a CSV file.

    Parameters:
    - file_path (str): The path to the CSV file.

    Returns:
    - pd.DataFrame: Loaded data as a pandas DataFrame.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at path: {file_path}")

    data = pd.read_csv(file_path)
    print(f"Data loaded successfully from {file_path}")

    return data

from sklearn.preprocessing import StandardScaler

def scale_data(data, label_column='label'):
    """
    Scales the dataset using StandardScaler, excluding the label column.

    Parameters:
    - data (pd.DataFrame): The input dataset.
    - label_column (str): The name of the column that holds the labels (default is 'label').

    Returns:
    - pd.DataFrame: Scaled dataset (excluding label column).
    - pd.DataFrame: The original label column (if exists).
    """
    if label_column in data.columns:
        # Separate features and labels
        labels = data[label_column]
        features = data.drop(columns=[label_column])
    else:
        features = data
        labels = None

    # Apply StandardScaler
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # Convert scaled features back to a DataFrame
    scaled_data = pd.DataFrame(scaled_features, columns=features.columns)

    if labels is not None:
        return scaled_data, labels
    else:
        return scaled_data


def load_and_scale_data(file_path, label_column='label'):
    """
    Loads and scales the dataset.

    Parameters:
    - file_path (str): Path to the preprocessed data file (CSV).
    - label_column (str): The name of the column to exclude from scaling (default is 'label').

    Returns:
    - pd.DataFrame: Scaled dataset.
    - pd.Series: Labels (if present).
    """
    # Load the data
    data = load_data(file_path)

    # Scale the data
    scaled_data, labels = scale_data(data, label_column)

    return scaled_data, labels
