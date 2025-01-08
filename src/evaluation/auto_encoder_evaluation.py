import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score


class AutoencoderEvaluation:
    def __init__(self, true_anomalies, predicted_anomalies, reconstruction_error):
        self.true_anomalies = true_anomalies
        self.predicted_anomalies = predicted_anomalies
        self.reconstruction_error = reconstruction_error

    def evaluate_precision(self):
        return precision_score(self.true_anomalies, self.predicted_anomalies)

    def evaluate_recall(self):
        return recall_score(self.true_anomalies, self.predicted_anomalies)

    def evaluate_f1_score(self):
        return f1_score(self.true_anomalies, self.predicted_anomalies)

    def evaluate_reconstruction_error(self):
        return np.mean(self.reconstruction_error)
