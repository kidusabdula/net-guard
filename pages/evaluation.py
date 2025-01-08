import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from preprocessing import (
    KMeansClustering,
    AutoencoderAnomalyDetector,
    KMeansEvaluation,
    AutoencoderEvaluation,
)
import matplotlib.pyplot as plt

st.set_page_config(page_title="Net Guard Anomaly Detection Evaluation", layout="wide")
st.title("Evaluation of Anomaly Detection Algorithms")

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

    true_anomalies = st.text_input(
        "Enter ground truth anomaly labels (comma-separated)", ""
    )

    if true_anomalies:
        true_anomalies = np.array([int(label) for label in true_anomalies.split(",")])

    if algorithm_choice == "K-Means Clustering":
        st.subheader("K-Means Clustering Evaluation")

        no_clusters = st.slider(
            "Select Number of Clusters", min_value=2, max_value=10, value=5
        )

        kmeans = KMeansClustering(no_clusters=no_clusters)
        results = kmeans.fit(scaled_data)

        evaluation = KMeansEvaluation(
            scaled_data, results["labels"], results["centroids"]
        )

        silhouette = evaluation.evaluate_silhouette()
        inertia = evaluation.evaluate_inertia()

        st.write(f"Silhouette Score: {silhouette}")
        st.write(f"Inertia: {inertia}")

    elif algorithm_choice == "Autoencoder":
        st.subheader("Autoencoder Evaluation")

        input_dim = scaled_data.shape[1]
        autoencoder = AutoencoderAnomalyDetector(input_dim=input_dim)
        autoencoder.build_autoencoder()
        autoencoder.train(scaled_data)

        anomalies = autoencoder.detect_anomalies(scaled_data)
        reconstruction_error = autoencoder.calculate_reconstruction_error(scaled_data)

        if true_anomalies.size > 0:
            evaluation = AutoencoderEvaluation(
                true_anomalies, anomalies, reconstruction_error
            )

            precision = evaluation.evaluate_precision()
            recall = evaluation.evaluate_recall()
            f1_score_val = evaluation.evaluate_f1_score()

            st.write(f"Precision: {precision}")
            st.write(f"Recall: {recall}")
            st.write(f"F1 Score: {f1_score_val}")

        st.write(f"Average Reconstruction Error: {np.mean(reconstruction_error)}")

    st.subheader("Evaluation Results Visualization")
    if algorithm_choice == "K-Means Clustering" and silhouette and inertia:
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))

        ax[0].bar(["Silhouette Score"], [silhouette], color="skyblue")
        ax[0].set_title("Silhouette Score")

        ax[1].bar(["Inertia"], [inertia], color="salmon")
        ax[1].set_title("Inertia")

        st.pyplot(fig)

    elif algorithm_choice == "Autoencoder" and reconstruction_error is not None:
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.hist(reconstruction_error, bins=50, color="green", alpha=0.7)
        ax.set_title("Reconstruction Error Distribution")
        st.pyplot(fig)

    st.sidebar.header("About Net Guard")
    st.sidebar.text(
        "This is an anomaly detection tool built using K-Means Clustering and Autoencoders."
    )
    st.sidebar.text("Select an algorithm to evaluate anomaly detection performance.")
