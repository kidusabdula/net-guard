import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from sklearn.preprocessing import MinMaxScaler

class AutoencoderAnomalyDetector:
    def __init__(self, input_dim, encoding_dim=64, epochs=50, batch_size=32, threshold_factor=2.5):
        """
        Initialize the Autoencoder for anomaly detection.

        Args:
            input_dim (int): Number of features in the input data.
            encoding_dim (int): Dimension of the encoded representation.
            epochs (int): Number of training epochs.
            batch_size (int): Batch size for training.
            threshold_factor (float): Multiplier for setting anomaly threshold.
        """
        self.input_dim = input_dim
        self.encoding_dim = encoding_dim
        self.epochs = epochs
        self.batch_size = batch_size
        self.threshold_factor = threshold_factor
        self.autoencoder = None
        self.threshold = None

    def build_autoencoder(self):
        """Build the autoencoder model."""
        input_layer = Input(shape=(self.input_dim,))
        encoded = Dense(self.encoding_dim, activation='relu')(input_layer)
        decoded = Dense(self.input_dim, activation='sigmoid')(encoded)
        self.autoencoder = Model(inputs=input_layer, outputs=decoded)
        self.autoencoder.compile(optimizer='adam', loss='mse')
        print("Autoencoder model built successfully.")

    def train(self, data):
        """
        Train the autoencoder on the scaled data.

        Args:
            data (np.ndarray): Scaled input data.
        """
        if self.autoencoder is None:
            raise ValueError("Autoencoder model is not built. Call `build_autoencoder()` first.")
        
        print("Training autoencoder...")
        self.autoencoder.fit(data, data, epochs=self.epochs, batch_size=self.batch_size, verbose=1)
        print("Autoencoder training completed.")

    def calculate_reconstruction_error(self, data):
        """
        Calculate reconstruction error for each data point.

        Args:
            data (np.ndarray): Scaled input data.

        Returns:
            np.ndarray: Reconstruction errors for each data point.
        """
        reconstructed = self.autoencoder.predict(data)
        return np.mean(np.abs(data - reconstructed), axis=1)

    def detect_anomalies(self, data):
        """
        Detect anomalies in the dataset.

        Args:
            data (np.ndarray): Scaled input data.

        Returns:
            np.ndarray: Boolean array indicating anomalies (True if anomalous).
        """
        reconstruction_error = self.calculate_reconstruction_error(data)
        self.threshold = np.mean(reconstruction_error) + self.threshold_factor * np.std(reconstruction_error)
        print(f"Anomaly threshold set to: {self.threshold}")
        return reconstruction_error > self.threshold

# Main function to integrate with main.py
def apply_autoencoder(scaled_data):
    """
    Apply autoencoder for anomaly detection on the scaled dataset.

    Args:
        scaled_data (np.ndarray): Scaled input data.
    """
    print("\nInitializing Autoencoder for Anomaly Detection...")
    input_dim = scaled_data.shape[1]
    autoencoder = AutoencoderAnomalyDetector(input_dim=input_dim)

    # Step 1: Build Autoencoder
    autoencoder.build_autoencoder()

    # Step 2: Train Autoencoder
    autoencoder.train(scaled_data)

    # Step 3: Detect Anomalies
    anomalies = autoencoder.detect_anomalies(scaled_data)

    # Step 4: Output Results
    print(f"Number of anomalies detected: {np.sum(anomalies)}")
    print("Anomaly detection completed. Returning results.")

    return anomalies

# Example integration in main.py

    
  
