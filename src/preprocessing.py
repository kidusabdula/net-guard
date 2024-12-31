import pandas as pd
import os
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, StandardScaler


import os
import pandas as pd
from typing import Optional, Tuple

def load_unsw_nb15_data(data_dir: str = "data") -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:

    train_path = os.path.join(data_dir, "UNSW_NB15_training-set.csv")
    test_path = os.path.join(data_dir, "UNSW_NB15_testing-set.csv")

    try:
        train_data = pd.read_csv(train_path)
        test_data = pd.read_csv(test_path)

        print(f"Training Data Loaded: {train_data.shape}")
        print(f"Testing Data Loaded: {test_data.shape}")

        return train_data, test_data
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return None, None
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file: {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None


def check_missing_values(data: pd.DataFrame, threshold: float = 0.0) -> pd.DataFrame:
    missing_count = data.isnull().sum()
    missing_percentage = (missing_count / len(data)) * 100
    missing_summary = pd.DataFrame({
        "Missing Count": missing_count,
        "Missing Percentage": missing_percentage
    })
    missing_summary = missing_summary[missing_summary["Missing Count"] > 0]
    missing_summary = missing_summary[missing_summary["Missing Percentage"] > threshold]

    if missing_summary.empty:
        print("No missing values found in the dataset.")
    else:
        print("Summary of Missing Values:")
        print(missing_summary)

    return missing_summary



def handle_missing_values(data):
    """
    Handles missing values in the dataset.

    Args:
        data (pd.DataFrame): The input dataset.

    Returns:
        pd.DataFrame: The dataset with missing values handled.
    """
    numeric_cols = data.select_dtypes(include=["float64", "int64"]).columns
    categorical_cols = data.select_dtypes(include=["object"]).columns

    # Handle missing values for numerical columns
    if len(numeric_cols) > 0:
        numeric_imputer = SimpleImputer(strategy="mean")
        data[numeric_cols] = numeric_imputer.fit_transform(data[numeric_cols])

    # Handle missing values for categorical columns
    if len(categorical_cols) > 0:
        categorical_imputer = SimpleImputer(strategy="most_frequent")
        data[categorical_cols] = categorical_imputer.fit_transform(
            data[categorical_cols]
        )
    return data


def encode_categorical_data(data):
    """
    Encodes categorical columns in the dataset using Label Encoding.

    Args:
        data (pd.DataFrame): The input dataset.

    Returns:
        pd.DataFrame: The dataset with encoded categorical features.
    """
    categorical_cols = data.select_dtypes(include=["object"]).columns
    label_encoder = LabelEncoder()

    for col in categorical_cols:
        data[col] = label_encoder.fit_transform(data[col])

    return data


def scale_numerical_data(data):
    """
    Scales numerical columns in the dataset using Standard Scaling,
    excluding 'id' and 'label' columns.

    Args:
        data (pd.DataFrame): The input dataset.

    Returns:
        pd.DataFrame: The dataset with scaled numerical features.
    """
    # Identify numerical columns
    numeric_cols = data.select_dtypes(include=["float64", "int64"]).columns

    # Exclude 'id' and 'label' columns
    numeric_cols_to_scale = [col for col in numeric_cols if col not in ["id", "label"]]

    # Initialize the scaler
    scaler = StandardScaler()

    # Apply scaling to the selected columns
    if len(numeric_cols_to_scale) > 0:
        data[numeric_cols_to_scale] = scaler.fit_transform(data[numeric_cols_to_scale])

    return data


def load_preprocessed_unsw_nb15_data(data_dir="data"):
    """
    Loads and preprocesses the UNSW-NB15 dataset.

    Args:
        data_dir (str): Directory containing the dataset CSV files.

    Returns:
        tuple: (processed_train_data, processed_test_data)
    """
    train_data, test_data = load_unsw_nb15_data(data_dir)

    if train_data is None or test_data is None:
        return None, None

    # Combine train and test datasets for consistent preprocessing
    combined_data = pd.concat([train_data, test_data], axis=0)

    # Step 1: Handle missing values
    combined_data = handle_missing_values(combined_data)

    # Step 2: Encode categorical data
    combined_data = encode_categorical_data(combined_data)

    # Step 3: Scale numerical data
    combined_data = scale_numerical_data(combined_data)

    # Separate back into train and test datasets
    processed_train_data = combined_data.iloc[: len(train_data), :].reset_index(
        drop=True
    )
    processed_test_data = combined_data.iloc[len(train_data) :, :].reset_index(
        drop=True
    )

    return processed_train_data, processed_test_data
