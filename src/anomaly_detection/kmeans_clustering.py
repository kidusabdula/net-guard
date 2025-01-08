import numpy as np
import pandas as pd


class KMeansClustering:
    def __init__(self, no_clusters=5, max_iter=100, tol=1e-4, random_state=42):
        self.n_clusters = no_clusters
        self.max_iter = max_iter
        self.tol = tol
        self.random_state = random_state
        self.centroids = None
        self.labels = None

    def _initialize_centroids(self, data):
        np.random.seed(self.random_state)
        indices = np.random.choice(data.shape[0], self.n_clusters, replace=False)
        return data.iloc[indices]

    def _assign_clusters(self, data, centroids):
        data_array = data.to_numpy() if isinstance(data, pd.DataFrame) else data
        centroids_array = (
            centroids.to_numpy() if isinstance(centroids, pd.DataFrame) else centroids
        )

        distances = np.linalg.norm(data_array[:, np.newaxis] - centroids_array, axis=2)
        return np.argmin(distances, axis=1)

    def _update_centroids(self, data, labels):
        return np.array(
            [data[labels == k].mean(axis=0) for k in range(self.n_clusters)]
        )

    def _has_converged(self, old_centroids, new_centroids):
        return np.all(np.abs(new_centroids - old_centroids) < self.tol)

    def fit(self, data):
        centroids = self._initialize_centroids(data)
        for iteration in range(self.max_iter):
            labels = self._assign_clusters(data, centroids)
            new_centroids = self._update_centroids(data, labels)
            if self._has_converged(centroids, new_centroids):
                break
            centroids = new_centroids

        self.centroids = centroids
        self.labels = labels
        return {"centroids": centroids, "labels": labels, "iterations": iteration + 1}

    def predict(self, data):
        distances = np.linalg.norm(data[:, np.newaxis] - self.centroids, axis=2)
        return np.argmin(distances, axis=1)
