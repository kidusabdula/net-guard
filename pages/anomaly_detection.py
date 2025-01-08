import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from anomaly_detection import kmeans_clustering
from preprocessing import AutoencoderAnomalyDetector

st.set_page_config(page_title="Net Guard Anomaly Detection", layout="wide")
st.title("Anomaly Detection with K-Means Clustering and Autoencoders")

uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head())

    st.subheader("Data Preprocessing")
    st.write("Scaling the data...")
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df.select_dtypes(include=[np.number]))

    algorithm_choice = st.selectbox(
        "Select Anomaly Detection Algorithm", ["K-Means Clustering", "Autoencoder"]
    )

    if algorithm_choice == "K-Means Clustering":
        st.subheader("K-Means Clustering")

        no_clusters = st.slider(
            "Select Number of Clusters", min_value=2, max_value=10, value=5
        )

        kmeans = kmeans_clustering(no_clusters=no_clusters)
        results = kmeans.fit(scaled_data)

        st.write(f"K-Means completed in {results['iterations']} iterations.")
        st.write(f"Centroids:\n{results['centroids']}")
        st.write(f"Sample Cluster Labels:\n{results['labels'][:10]}")

        if scaled_data.shape[1] == 2:
            st.subheader("Cluster Visualization")
            fig, ax = plt.subplots()
            ax.scatter(
                scaled_data[:, 0],
                scaled_data[:, 1],
                c=results["labels"],
                cmap="viridis",
            )
            ax.scatter(
                results["centroids"][:, 0],
                results["centroids"][:, 1],
                marker="X",
                s=200,
                c="red",
            )
            ax.set_title("K-Means Clusters")
            st.pyplot(fig)

    elif algorithm_choice == "Autoencoder":
        st.subheader("Autoencoder Anomaly Detection")

        input_dim = scaled_data.shape[1]
        autoencoder = AutoencoderAnomalyDetector(input_dim=input_dim)
        autoencoder.build_autoencoder()
        autoencoder.train(scaled_data)

        anomalies = autoencoder.detect_anomalies(scaled_data)
        st.write(f"Number of anomalies detected: {np.sum(anomalies)}")

        st.subheader("Anomaly Detection Visualization")
        fig, ax = plt.subplots()
        ax.scatter(
            range(len(scaled_data)), scaled_data[:, 0], c=anomalies, cmap="coolwarm"
        )
        ax.set_title("Anomaly Detection Results")
        ax.set_xlabel("Sample Index")
        ax.set_ylabel("Feature 1 Value")
        st.pyplot(fig)

    st.sidebar.header("About Net Guard")
    st.sidebar.text(
        "This is an anomaly detection tool built using K-Means Clustering and Autoencoders."
    )
    st.sidebar.text("Select an algorithm to detect anomalies in your dataset.")
