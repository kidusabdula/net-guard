import numpy as np
import pandas as pd

class KMeansClustering:
    def __init__(self, no_clusters=5, max_iter=100, tol=1e-4, random_state=42):
        """
        Initialize K-Means Clustering parameters.

        Args:
            n_clusters (int): Number of clusters (default 5).
            max_iter (int): Maximum iterations (default 100).
            tol (float): Convergence tolerance (default 1e-4).
            random_state (int): Random seed for reproducibility (default 42).
        """
        self.n_clusters = no_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        self.centroids = None
        self.labels = None

    def _initialize_centroids(self, data):
        """Randomly initialize centroids."""
        np.random.seed(self.random_state)
        indices = np.random.choice(data.shape[0], self.n_clusters, replace=False)
        return data.iloc[indices]

    def _assign_clusters(self, data, centroids):
        """
        Assign each data point to the nearest cluster.
        """
        # Ensure data and centroids are NumPy arrays for calculations
        data_array = data.to_numpy() if isinstance(data, pd.DataFrame) else data
        centroids_array = centroids.to_numpy() if isinstance(centroids, pd.DataFrame) else centroids

        # Calculate distances using broadcasting
        distances = np.linalg.norm(data_array[:, np.newaxis] - centroids_array, axis=2)
        return np.argmin(distances, axis=1)  # Return the index of the nearest centroid

    def _update_centroids(self, data, labels):
        """Compute new centroids as the mean of assigned points."""
        return np.array([data[labels == k].mean(axis=0) for k in range(self.n_clusters)])

    def _has_converged(self, old_centroids, new_centroids):
        """Check if centroids have converged based on tolerance."""
        return np.all(np.abs(new_centroids - old_centroids) < self.tol)

    def fit(self, data):
        """
        Apply K-Means clustering to the dataset.

        Args:
            data (np.ndarray): Scaled dataset (n_samples, n_features).

        Returns:
            dict: Clustering results containing centroids, labels, and iterations.
        """
        centroids = self._initialize_centroids(data)
        for iteration in range(self.max_iter):
            labels = self._assign_clusters(data, centroids)
            new_centroids = self._update_centroids(data, labels)
            if self._has_converged(centroids, new_centroids):
                break
            centroids = new_centroids

        self.centroids = centroids
        self.labels = labels
        return {
            "centroids": centroids,
            "labels": labels,
            "iterations": iteration + 1
        }

    def predict(self, data):
        """
        Predict cluster labels for new data points.

        Args:
            data (np.ndarray): New data (n_samples, n_features).

        Returns:
            np.ndarray: Predicted cluster labels.
        """
        distances = np.linalg.norm(data[:, np.newaxis] - self.centroids, axis=2)
        return np.argmin(distances, axis=1)
