import pandas as pd
import os


def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at path: {file_path}")

    data = pd.read_csv(file_path)
    print(f"Data loaded successfully from {file_path}")

    return data


from sklearn.preprocessing import StandardScaler


def scale_data(data, label_column="label"):
    if label_column in data.columns:
        labels = data[label_column]
        features = data.drop(columns=[label_column])
    else:
        features = data
        labels = None

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    scaled_data = pd.DataFrame(scaled_features, columns=features.columns)

    if labels is not None:
        return scaled_data, labels
    else:
        return scaled_data


def load_and_scale_data(file_path, label_column="label"):
    data = load_data(file_path)

    scaled_data, labels = scale_data(data, label_column)

    return scaled_data, labels
