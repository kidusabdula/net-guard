import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def plot_clusters(data, labels, centroids):
    plt.figure(figsize=(10, 7))
    unique_labels = np.unique(labels)
    for label in unique_labels:
        plt.scatter(
            data[labels == label, 0], data[labels == label, 1], label=f"Cluster {label}"
        )
    plt.scatter(
        centroids[:, 0], centroids[:, 1], s=300, c="red", label="Centroids", marker="X"
    )
    plt.legend()
    plt.title("K-Means Clustering")
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.show()
