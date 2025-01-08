import numpy as np
import tensorflow as tf
from keras import Model
from keras import Input, Dense
from sklearn.preprocessing import MinMaxScaler


class AutoencoderAnomalyDetector:
    def __init__(
        self, input_dim, encoding_dim=64, epochs=50, batch_size=32, threshold_factor=2.5
    ):
        self.input_dim = input_dim
        self.encoding_dim = encoding_dim
        self.epochs = epochs
        self.batch_size = batch_size
        self.threshold_factor = threshold_factor
        self.autoencoder = None
        self.threshold = None

    def build_autoencoder(self):
        input_layer = Input(shape=(self.input_dim,))
        encoded = Dense(self.encoding_dim, activation="relu")(input_layer)
        decoded = Dense(self.input_dim, activation="sigmoid")(encoded)
        self.autoencoder = Model(inputs=input_layer, outputs=decoded)
        self.autoencoder.compile(optimizer="adam", loss="mse")
        print("Autoencoder model built successfully.")

    def train(self, data):
        if self.autoencoder is None:
            raise ValueError(
                "Autoencoder model is not built. Call `build_autoencoder()` first."
            )

        print("Training autoencoder...")
        self.autoencoder.fit(
            data, data, epochs=self.epochs, batch_size=self.batch_size, verbose=1
        )
        print("Autoencoder training completed.")

    def calculate_reconstruction_error(self, data):
        reconstructed = self.autoencoder.predict(data)
        return np.mean(np.abs(data - reconstructed), axis=1)

    def detect_anomalies(self, data):
        reconstruction_error = self.calculate_reconstruction_error(data)
        self.threshold = np.mean(reconstruction_error) + self.threshold_factor * np.std(
            reconstruction_error
        )
        print(f"Anomaly threshold set to: {self.threshold}")
        return reconstruction_error > self.threshold


def apply_autoencoder(scaled_data):
    print("\nInitializing Autoencoder for Anomaly Detection...")
    input_dim = scaled_data.shape[1]
    autoencoder = AutoencoderAnomalyDetector(input_dim=input_dim)

    autoencoder.build_autoencoder()

    autoencoder.train(scaled_data)

    anomalies = autoencoder.detect_anomalies(scaled_data)

    print(f"Number of anomalies detected: {np.sum(anomalies)}")
    print("Anomaly detection completed. Returning results.")

    return anomalies
