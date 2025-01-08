import numpy as np
from scipy.spatial.distance import cdist

class KNNImputerFactory:
    
    def __init__(self, n_neighbors=5, metric='euclidean', aggregation='mean'):
        """
        Initialize the KNN Imputer.

        Args:
            n_neighbors (int): Number of neighbors to consider.
            metric (str): Distance metric ('euclidean', 'manhattan', etc.).
            aggregation (str): Aggregation method ('mean', 'median', 'mode').
        """
        self.n_neighbors = n_neighbors
        self.metric = metric
        self.aggregation = aggregation

    def _compute_distances(self, X, target_row):
        """
        Compute distances between the target row and all other rows in X.

        Args:
            X (ndarray): Dataset without missing values.
            target_row (ndarray): Row with missing values.

        Returns:
            distances (ndarray): Array of distances.
        """
        mask = ~np.isnan(target_row)  # Ignore missing features
        valid_X = X[:, mask]
        valid_target_row = target_row[mask]
        distances = cdist(valid_X, valid_target_row.reshape(1, -1), metric=self.metric).flatten()
        return distances

    def _aggregate(self, values):
        """
        Aggregate values using the specified method.

        Args:
            values (ndarray): Array of values to aggregate.

        Returns:
            Aggregated value.
        """
        if self.aggregation == 'mean':
            return np.nanmean(values)
        elif self.aggregation == 'median':
            return np.nanmedian(values)
        elif self.aggregation == 'mode':
            return np.bincount(values).argmax()  # For categorical data
        else:
            raise ValueError("Unsupported aggregation method")

    def fit_transform(self, X):
        """
        Impute missing values in the dataset.

        Args:
            X (ndarray): Dataset with missing values.

        Returns:
            X_imputed (ndarray): Dataset with imputed values.
        """
        X = np.array(X, dtype=float)  # Ensure numerical processing
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                if np.isnan(X[i, j]):
                    distances = self._compute_distances(X[~np.isnan(X[:, j])], X[i])
                    neighbor_indices = np.argsort(distances)[:self.n_neighbors]
                    neighbor_values = X[neighbor_indices, j]
                    X[i, j] = self._aggregate(neighbor_values)
        return X

