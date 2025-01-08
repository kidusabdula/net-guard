import pandas as pd
from sklearn.preprocessing import LabelEncoder
import logging
import numpy as np


class DatasetDecoderFactory:
    def __init__(self, dataset, threshold=10):
        self.dataset = dataset
        self.threshold = threshold
        self.one_hot_columns = self.detect_one_hot_columns()
        self.label_encoders = self.detect_label_encoders()

    def detect_one_hot_columns(self):
        one_hot_columns = {}
        for col in self.dataset.columns:
            base_col = col.split("_")[0]
            if base_col not in one_hot_columns:
                one_hot_group = [
                    c for c in self.dataset.columns if c.startswith(f"{base_col}_")
                ]
                if len(one_hot_group) > 0:
                    one_hot_columns[base_col] = one_hot_group
        return one_hot_columns

    def detect_label_encoders(self):
        label_encoders = {}
        for col in self.dataset.columns:
            unique_values = self.dataset[col].nunique()
            if unique_values <= self.threshold and col not in sum(
                self.one_hot_columns.values(), []
            ):
                encoder = LabelEncoder()
                encoder.classes_ = np.array(sorted(self.dataset[col].dropna().unique()))
                label_encoders[col] = encoder
        return label_encoders

    def decode_one_hot(self, data):
        decoded_columns = {}
        for feature, columns in self.one_hot_columns.items():
            categories = [col.split(f"{feature}_")[1] for col in columns]
            categories = ["Unknown"] + categories
            decoded_columns[feature] = pd.Categorical(
                data[columns]
                .idxmax(axis=1)
                .str.replace(f"{feature}_", "", regex=False),
                categories=categories,
            ).fillna(categories[0])

        data = data.drop(
            columns=[col for cols in self.one_hot_columns.values() for col in cols]
        )
        for feature, decoded_col in decoded_columns.items():
            data[feature] = decoded_col

        return data

    def decode_label(self, data):
        for feature, encoder in self.label_encoders.items():
            encoder.fit(data[feature].astype(str))
            try:
                data[feature] = encoder.inverse_transform(data[feature].astype(int))
            except ValueError as e:
                print(f"Warning: {e} for column {feature}")
        return data

    def decode(self, data):
        data = self.decode_one_hot(data)
        data = self.decode_label(data)
        return data
