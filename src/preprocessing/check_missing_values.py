import pandas as pd
from typing import Tuple


def check_missing_values_module(
    test_data: pd.DataFrame, train_data: pd.DataFrame, threshold: float = 0.0
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Check for missing values in test and train datasets and return their summaries.

    Args:
        test_data (pd.DataFrame): Test dataset.
        train_data (pd.DataFrame): Train dataset.
        threshold (float): Percentage threshold to consider for reporting missing values.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: Summaries of missing values in test and train datasets.
    """
    # Test Data Summary
    test_data_missing_summary = test_data.isnull().mean() * 100
    test_data_missing_summary = test_data_missing_summary[
        test_data_missing_summary > threshold
    ].to_frame(name="Missing Percentage in test data")

    # Train Data Summary
    train_data_missing_summary = train_data.isnull().mean() * 100
    train_data_missing_summary = train_data_missing_summary[
        train_data_missing_summary > threshold
    ].to_frame(name="Missing Percentage in train data")

    # Logging Information
    if not test_data_missing_summary.empty:
        print("Missing values found in test dataset.")
    else:
        print("No missing values in test dataset.")

    if not train_data_missing_summary.empty:
        print("Missing values found in train dataset.")
    else:
        print("No missing values in train dataset.")

    print("\nSummary of Missing Values in Test Dataset:")
    print(test_data_missing_summary)

    print("\nSummary of Missing Values in Train Dataset:")
    print(train_data_missing_summary)

    return test_data_missing_summary, train_data_missing_summary


def check_missing_values_after_imputation(
    df_imputed: pd.DataFrame, threshold: float = 0.0
) -> Tuple[pd.DataFrame]:
    check_missing_values_after_imputation_summary = df_imputed.isnull().mean() * 100
    check_missing_values_after_imputation_summary = (
        check_missing_values_after_imputation_summary[
            check_missing_values_after_imputation_summary > threshold
        ].to_frame(name="Missing Data after imputation")
    )

    if not check_missing_values_after_imputation_summary.empty:
        print("Mising values still exist")
    else:
        print("No missing values, Imputation Worked")
        
    return check_missing_values_after_imputation_summary