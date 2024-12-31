import pandas as pd
from load_dataset import load_unsw_nb15_data
from check_missing_values import check_missing_values_module, check_missing_values_after_imputation
from encoding import DatasetEncoder
from knnimputer import KNNImputerCustom
from data_decoder import data_decoder
from pre_processed_data_loading_scaling import load_and_scale_data
import os
import matplotlib.pyplot as plt 
from KMeansClustering import KMeansClustering
from utilis import plot_clusters
from autoencoderanomalydetector import apply_autoencoder

def load_and_process_data():
    # Step 1: Load the dataset
    test_df, train_df, combined_df = load_unsw_nb15_data()  # Returns the combined DataFrame
    if train_df is None or test_df is None or combined_df is None:
        print("Failed to load the dataset. Exiting...")
        return

    print("Dataset loaded successfully")

  # Step 2: Check for missing values
    print("\nChecking missing values...")
    test_data_missing_summary, train_data_missing_summary = check_missing_values_module(
        test_df, train_df
    )

    #Ensure the summaries are used correctly
    if not test_data_missing_summary.empty:
        print("\nMissing Values in Test Data Columns:")
        print(test_data_missing_summary)

    if not train_data_missing_summary.empty:
        print("\nMissing Values in Train Data Columns:")
        print(train_data_missing_summary)

    # Step 3: Encode categorical data
    encoder = DatasetEncoder(combined_df)
    encoded_df = (
        encoder.apply_encoding()
    )  # Automatically detects and encodes based on unique value count
    print("\nEncoding completed:")
    print(encoded_df.head())  # Show a preview of the encoded dataset
    encoded_output_file = os.path.join('data', 'encoded_pre_processed_data.csv')
    encoded_df.to_csv(encoded_output_file, index=False)  # Saving without the index column
    print(f"\nEncoded data has been saved to {encoded_output_file}")

    # Step 4: Apply KNN Imputation
    print("\nPerforming KNN Imputation...")
    imputer = KNNImputerCustom(n_neighbors=5, metric="euclidean", aggregation="mean")
    imputed_data = imputer.fit_transform(encoded_df.values)
    df_imputed = pd.DataFrame(imputed_data, columns=encoded_df.columns)
    print("\nKNN Imputation completed:")
    print(df_imputed.head())  # Show a preview of the imputed data
    check_imputed_df_summary = check_missing_values_after_imputation(df_imputed)
    #print("Check missing values after imputation")
    print(check_imputed_df_summary.head())
    #return df_imputed  # Return the final processed dataset


    # Step 5: Decode the imputed data
    print("\nDecoding the imputed data...")
    decoder = data_decoder(df_imputed)  # Automated column detection
    decoded_data = decoder.decode(df_imputed)
    print("\nDecoding completed.")
    print(decoded_data.head(100))  # Show a preview of the decoded dataset

    output_file = os.path.join('data', 'pre_processed_data.csv')
    decoded_data.to_csv(output_file, index=False)  # Saving without the index column
    print(f"\nDecoded data has been saved to {output_file}")
    
    # Step 6: Load and Scale pre processed data
    print("\n Loading and Scaling pre-processed data")
    scaled_data, labels = load_and_scale_data(encoded_output_file)
    # Display scaled data and labels
    print("\nScaled Data (first 100 rows):")
    print(pd.DataFrame(scaled_data).head(30).describe())  # Convert NumPy array to DataFrame for readability
    #pd.DataFrame(scaled_data, columns=scaled_data.columns).hist(figsize=(20, 15), bins=20)
    plt.show()

    print("\nLabels (first 5):")
    print(labels[:5])  # Show the first 5 labels
    
    scaled_data_output_file = os.path.join('data', 'scaled_data.csv')
    scaled_data.to_csv(scaled_data_output_file, index=False)  # Saving without the index column
    print(f"\nDecoded data has been saved to {scaled_data_output_file}")
    
    # Step 7: Perform K-means clustering 
    print("\n K-means clustering initiated")
    no_clusters= 5
    kmeans = KMeansClustering(no_clusters = no_clusters)
    results = kmeans.fit(scaled_data)

    centroids = results["centroids"]
    labels = results["labels"]
    iterations = results["iterations"]
    
    print(f"\nK-Means Clustering completed in {iterations} iterations.")
    print(f"Centroids:\n{centroids}")
    print(f"Sample Cluster Labels:\n{labels[:10]}")

    # Optional: Visualize clusters (for 2D data)
    if scaled_data.shape[1] == 2:
        plot_clusters(scaled_data, labels, centroids)
        
    # Step 8: Apply Autoencoders to detect anomalies
 
    apply_autoencoder(scaled_data)
  


if __name__ == "__main__":
    load_and_process_data()
 