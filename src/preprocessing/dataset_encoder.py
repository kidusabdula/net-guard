import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

class DatasetEncoderFactory:
    def __init__(self, dataset):
        self.dataset = dataset
        self.label_encoder = LabelEncoder()
        self.one_hot_encoder = OneHotEncoder(sparse_output=False, drop='first') 

    def encode_label(self, column):
        self.dataset[column] = self.label_encoder.fit_transform(self.dataset[column])
        return self.dataset

    def encode_one_hot(self, column):
        encoded_data = self.one_hot_encoder.fit_transform(self.dataset[column].values.reshape(-1, 1))
        encoded_df = pd.DataFrame(
            encoded_data, 
            columns=[f"{column}_{category}" for category in self.one_hot_encoder.categories_[0][1:]]  
        )
        self.dataset = pd.concat([self.dataset, encoded_df], axis=1)
        self.dataset.drop(columns=[column], inplace=True)
        return self.dataset

    def detect_and_encode(self):
        for column in self.dataset.select_dtypes(include=['object']).columns:
            unique_values = self.dataset[column].nunique()
            if unique_values <= 10:
                print(f"Applying Label Encoding to column: {column}")
                self.encode_label(column)
            else:
                print(f"Applying One-Hot Encoding to column: {column}")
                self.encode_one_hot(column)
        
        return self.dataset

    def apply_encoding(self):
        return self.detect_and_encode()
