from sklearn.metrics import silhouette_score
from sklearn.metrics import mean_squared_error
import numpy as np


class KMeansEvaluation:
    def __init__(self, data, labels, centroids):
        self.data = data
        self.labels = labels
        self.centroids = centroids

    def evaluate_silhouette(self):
        return silhouette_score(self.data, self.labels)

    def evaluate_inertia(self):
        inertia = 0
        for i in range(self.centroids.shape[0]):
            cluster_points = self.data[self.labels == i]
            inertia += np.sum((cluster_points - self.centroids[i]) ** 2)
        return inertia
