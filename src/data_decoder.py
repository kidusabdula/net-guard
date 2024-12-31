import pandas as pd
from sklearn.preprocessing import LabelEncoder
import logging
import numpy as np


class data_decoder:
    def __init__(self, dataset, threshold=10):
        """
        Initialize the UNSWDecoder with the dataset to detect encodings.
        
        :param dataset: The DataFrame containing encoded data.
        :param threshold: Maximum number of unique values to treat as label-encoded.
        """
        self.dataset = dataset
        self.threshold = threshold
        self.one_hot_columns = self.detect_one_hot_columns()
        self.label_encoders = self.detect_label_encoders()

    def detect_one_hot_columns(self):
        """
        Automatically detect one-hot encoded columns based on naming patterns.
        
        :return: Dictionary mapping features to their one-hot encoded column names.
        """
        one_hot_columns = {}
        for col in self.dataset.columns:
            base_col = col.split("_")[0]
            if base_col not in one_hot_columns:
                one_hot_group = [
                    c for c in self.dataset.columns if c.startswith(f"{base_col}_")
                ]
                if len(one_hot_group) > 0:  # Ensure it's one-hot encoded with drop='first'
                    one_hot_columns[base_col] = one_hot_group
        return one_hot_columns

    def detect_label_encoders(self):
        """
        Automatically detect label-encoded columns based on the threshold for unique values.
        
        :return: Dictionary mapping features to fitted LabelEncoder instances.
        """
        label_encoders = {}
        for col in self.dataset.columns:
            unique_values = self.dataset[col].nunique()
            if unique_values <= self.threshold and col not in sum(self.one_hot_columns.values(), []):
                encoder = LabelEncoder()
                encoder.classes_ = np.array(sorted(self.dataset[col].dropna().unique()))
                label_encoders[col] = encoder
        return label_encoders

    def decode_one_hot(self, data):
        """
        Decode one-hot encoded columns back to their original categorical values.
        
        :param data: DataFrame with one-hot encoded features.
        :return: DataFrame with decoded features.
        """
        decoded_columns = {}
        for feature, columns in self.one_hot_columns.items():
            # Handle missing category due to drop='first'
            categories = [col.split(f"{feature}_")[1] for col in columns]
            categories = ["Unknown"] + categories  # Include the dropped category as None
            decoded_columns[feature] = pd.Categorical(
                data[columns].idxmax(axis=1).str.replace(f"{feature}_", "", regex=False),
                categories=categories,
            ).fillna(categories[0])

        # Drop one-hot encoded columns and add decoded features
        data = data.drop(columns=[col for cols in self.one_hot_columns.values() for col in cols])
        for feature, decoded_col in decoded_columns.items():
            data[feature] = decoded_col

        return data

    def decode_label(self, data):
        for feature, encoder in self.label_encoders.items():
            # Re-fit encoder on the entire data to handle unseen labels
            encoder.fit(data[feature].astype(str))  # Fit the encoder to the entire column
            try:
                # Decode values (inverse transform)
                data[feature] = encoder.inverse_transform(data[feature].astype(int))
            except ValueError as e:
                print(f"Warning: {e} for column {feature}")
                # Optionally, handle unseen labels here, for example by keeping them as is
        return data

    def decode(self, data):
        """
        Decode both one-hot and label-encoded features.
        
        :param data: DataFrame with encoded features.
        :return: Fully decoded DataFrame.
        """
        data = self.decode_one_hot(data)
        data = self.decode_label(data)
        return data
