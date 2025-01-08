import pandas as pd
from preprocessing.load_raw_data import raw_dataset_loader
from preprocessing.check_missing_values import (
    check_missing_values_module,
    check_missing_values_after_imputation,
)
from preprocessing.dataset_encoder import DatasetEncoder
from anomaly_detection.knn_imputation import KNNImputerCustom
from preprocessing.dataset_decoder import data_decoder
from preprocessing.pre_processed_data_loading_scaling import load_and_scale_data
import os
import matplotlib.pyplot as plt
from anomaly_detection.kmeans_clustering import KMeansClustering
from utils.utilis import plot_clusters
from anomaly_detection.auto_encoder import apply_autoencoder
from database.db_operations import fetch_table_data


def load_and_process_data():

    print("Current Working Directory:", os.getcwd())
    try:
        train_df, test_df, combined_df = raw_dataset_loader()
        print(test_df.describe())
        for column in test_df.columns:
            if test_df[column].dtype in ["int64", "float64"]:
                max_value = test_df[column].max()
                print(f"Column {column}: Max Value = {max_value}")

    except ValueError as e:
        print(
            f"Error loading data: {e}. Please check the load_unsw_nb15_data function."
        )
        return
    except FileNotFoundError as e:
        print(
            f"File not found: {e}. Please ensure the dataset is in the correct directory."
        )
        return

    if train_df is None or test_df is None:
        print("Failed to load the dataset. Exiting...")
        return

    print("Dataset loaded successfully")

    print("Fetching train and test datasets from the database...")
    fetched_train_df = fetch_table_data("unsw_nb15_raw_train_dataset")
    fetched_test_df = fetch_table_data("unsw_nb15_raw_test_dataset")

    print("\nChecking missing values...")
    test_data_missing_summary, train_data_missing_summary = check_missing_values_module(
        fetched_test_df, fetched_train_df
    )

    if not test_data_missing_summary.empty:
        print("\nMissing Values in Test Data Columns:")
        print(test_data_missing_summary)

    if not train_data_missing_summary.empty:
        print("\nMissing Values in Train Data Columns:")
        print(train_data_missing_summary)

    data_folder = os.path.join(os.getcwd(), "data")
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        print(f"Created 'data' folder at {data_folder}")

    encoder = DatasetEncoder(fetched_train_df)
    encoded_df = encoder.apply_encoding() 
    print("\nEncoding completed:")
    print(encoded_df.head()) 

    encoded_output_file = os.path.join(data_folder, "encoded_df.csv")
    encoded_df.to_csv(
        encoded_output_file, index=False
    )  
    print(f"\nEncoded data has been saved to {encoded_output_file}")

    print("\nPerforming KNN Imputation...")
    imputer = KNNImputerCustom(n_neighbors=5, metric="euclidean", aggregation="mean")
    imputed_data = imputer.fit_transform(encoded_df.values)
    df_imputed = pd.DataFrame(imputed_data, columns=encoded_df.columns)
    print("\nKNN Imputation completed:")
    print(df_imputed.head())  
    check_imputed_df_summary = check_missing_values_after_imputation(df_imputed)
    print(check_imputed_df_summary.head())

    
    print("\nDecoding the imputed data...")
    decoder = data_decoder(df_imputed)  
    decoded_data = decoder.decode(df_imputed)
    print("\nDecoding completed.")
    print(decoded_data.head(100))  

    output_file = os.path.join("data", "pre_processed_data.csv")
    decoded_data.to_csv(output_file, index=False) 
    print(f"\nDecoded data has been saved to {output_file}")

    print("\n Loading and Scaling pre-processed data")
    scaled_data, labels = load_and_scale_data(encoded_output_file)
    print("\nScaled Data (first 100 rows):")
    print(
        pd.DataFrame(scaled_data).head(30).describe()
    ) 
    plt.show()

    print("\nLabels (first 5):")
    print(labels[:5])  

    scaled_data_output_file = os.path.join("data", "scaled_data.csv")
    scaled_data.to_csv(
        scaled_data_output_file, index=False
    )  
    print(f"\nDecoded data has been saved to {scaled_data_output_file}")

    print("\n K-means clustering initiated")
    no_clusters = 5
    kmeans = KMeansClustering(no_clusters=no_clusters)
    results = kmeans.fit(scaled_data)

    centroids = results["centroids"]
    labels = results["labels"]
    iterations = results["iterations"]

    print(f"\nK-Means Clustering completed in {iterations} iterations.")
    print(f"Centroids:\n{centroids}")
    print(f"Sample Cluster Labels:\n{labels[:10]}")

    if scaled_data.shape[1] == 2:
        plot_clusters(scaled_data, labels, centroids)


    apply_autoencoder(scaled_data)


if __name__ == "__main__":
    load_and_process_data()
