import numpy as np
from scipy.spatial.distance import cdist


class KNNImputerFactory:

    def __init__(self, n_neighbors=5, metric="euclidean", aggregation="mean"):
        self.n_neighbors = n_neighbors
        self.metric = metric
        self.aggregation = aggregation

    def _compute_distances(self, X, target_row):
        mask = ~np.isnan(target_row)
        valid_X = X[:, mask]
        valid_target_row = target_row[mask]
        distances = cdist(
            valid_X, valid_target_row.reshape(1, -1), metric=self.metric
        ).flatten()
        return distances

    def _aggregate(self, values):
        if self.aggregation == "mean":
            return np.nanmean(values)
        elif self.aggregation == "median":
            return np.nanmedian(values)
        elif self.aggregation == "mode":
            return np.bincount(values).argmax()
        else:
            raise ValueError("Unsupported aggregation method")

    def fit_transform(self, X):
        X = np.array(X, dtype=float)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                if np.isnan(X[i, j]):
                    distances = self._compute_distances(X[~np.isnan(X[:, j])], X[i])
                    neighbor_indices = np.argsort(distances)[: self.n_neighbors]
                    neighbor_values = X[neighbor_indices, j]
                    X[i, j] = self._aggregate(neighbor_values)
        return X
