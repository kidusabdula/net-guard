```markdown
# Net Guard - Anomaly Detection for Network Security Logs

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setting Up the Environment](#setting-up-the-environment)
  - [Installing Dependencies](#installing-dependencies)
- [Running the Project](#running-the-project)
  - [Starting the Streamlit Dashboard](#starting-the-streamlit-dashboard)
  - [Uploading Data](#uploading-data)
- [Evaluation and Metrics](#evaluation-and-metrics)
  - [K-Means Clustering Evaluation](#k-means-clustering-evaluation)
  - [Autoencoder Evaluation](#autoencoder-evaluation)
- [Data Preprocessing](#data-preprocessing)
- [Model Training](#model-training)
  - [K-Means Clustering](#k-means-clustering)
  - [Autoencoder](#autoencoder)
- [Visualization Dashboard](#visualization-dashboard)
- [Testing and Validation](#testing-and-validation)
- [Contributing](#contributing)
- [License](#license)

## Introduction

**Net Guard** is an advanced **anomaly detection system** designed to identify unusual patterns and potential security breaches in network logs. By leveraging machine learning models like **K-Means Clustering** and **Autoencoders**, this project aims to enhance cybersecurity by detecting anomalies such as unauthorized access, data breaches, malware activity, and other malicious patterns in network traffic.

The project focuses on detecting anomalies in real-time network logs through a **preprocessing pipeline**, **model training**, and an **interactive dashboard**. It uses a dataset from the **UNSW-NB15** collection, known for its wide variety of network traffic anomalies.

## Features

- **Anomaly Detection**: Identifies anomalous network traffic using K-Means Clustering and Autoencoders.
- **Real-time Data Preprocessing**: Handles missing data, scales features, and prepares data for model training.
- **Model Evaluation**: Evaluates the performance of the anomaly detection algorithms using metrics like precision, recall, F1-score, silhouette score, and inertia.
- **Interactive Visualization**: A user-friendly **Streamlit dashboard** that allows easy data upload, model evaluation, and visualization of results.
- **Data Exploration**: Displays the first few rows of the dataset for insights and easy data inspection.
  
## Technology Stack

- **Backend**:
  - Python 3.x
  - Scikit-learn (for K-Means and clustering)
  - TensorFlow/Keras (for Autoencoder models)
  - Pandas (for data manipulation)
  - NumPy (for numerical operations)
  - Streamlit (for the frontend/dashboard)

- **Frontend**:
  - Streamlit (used for building the interactive dashboard)
  
- **Data Handling**:
  - UNSW-NB15 dataset (real-world network traffic data)
  
- **Development Tools**:
  - Git for version control
  - Virtualenv or Conda for environment management

## Project Structure

```
NetGuard/
├── src/
│   ├── __init__.py
│   ├── Preprocessing/
│   │   ├── __init__.py
│   │   ├── data_preprocessing.py        # Data loading, scaling, missing value handling
│   │   └── data_cleaning.py             # Cleaning and preprocessing logic
│   ├── Models/
│   │   ├── kmeans_clustering.py         # KMeans model
│   │   ├── autoencoder.py               # Autoencoder model
│   │   └── evaluation.py                # Evaluation logic for models
│   └── Streamlit/
│       └── app.py                       # Streamlit dashboard script
├── README.md                            # Project documentation
└── .gitignore                           # Git ignore file
```

## Installation

Setting up **Net Guard** involves several key steps, ranging from preparing your system to managing virtual environments and installing dependencies. Below, we detail the full installation process. Follow each step carefully to ensure that all dependencies are installed properly and that your environment is correctly configured to run the project smoothly.

### Prerequisites

Before beginning installation, ensure that your system meets the following requirements:

1. **Python 3.x**:
   Ensure that you are running **Python 3.14** or higher. To verify your Python version, run:
    ```bash
    python --version
    ```
   If Python is not installed, download it from the [official Python website](https://www.python.org/downloads/), and follow the installation instructions for your operating system. During installation, **ensure that Python is added to your system's PATH** to avoid issues with command-line access.

2. **Git**:
   To clone the repository and manage versions, Git must be installed. Check if Git is available by running:
    ```bash
    git --version
    ```
   If not, you can download it from [Git’s official website](https://git-scm.com/downloads) and follow the installation instructions. Windows users are encouraged to use **Git Bash** for a better command-line experience.

3. **Virtual Environment Management (Optional but Recommended)**:
   It is strongly recommended to set up a virtual environment for dependency management. Virtualenv and Conda are the most common tools to manage project-specific dependencies:

   - **Virtualenv**:
     Install it globally using:
     ```bash
     pip install virtualenv
     ```
     Create a virtual environment in your project directory:
     ```bash
     virtualenv venv
     ```
     Activate it:
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```

   - **Conda**:
     If you prefer Conda for environment management, install Anaconda from [here](https://www.anaconda.com/products/distribution), or Miniconda from [here](https://docs.conda.io/en/latest/miniconda.html). Once installed, you can create and activate a new environment with:
     ```bash
     conda create --name netguard python=3.8
     conda activate netguard
     ```

4. **PostgreSQL** (Optional, for database interaction):
   If the project includes data persistence or interaction with PostgreSQL, make sure that **PostgreSQL** is installed. Verify its installation by running:
    ```bash
    psql -V
    ```
   If PostgreSQL is not installed, download it from the [official PostgreSQL website](https://www.postgresql.org/download/) and follow the installation steps. Once installed, you may need to configure the PostgreSQL service to start automatically on system boot.

### Setting Up the Environment

#### 1. Clone the Repository

Start by cloning the project repository to your local machine. Use `git` to download the project files:
```bash
git clone https://github.com/kidusabdula/net-guard.git
cd netguard
```
If you are using HTTPS or SSH for cloning, ensure that your Git configuration is correct and that you have the appropriate access to the repository.

#### 2. Set Up a Virtual Environment

Navigate to your project directory and create a virtual environment. This keeps your project dependencies isolated from other system-wide installations.

- **For Virtualenv**:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
  ```

- **For Conda**:
  ```bash
  conda create --name netguard python=3.8
  conda activate netguard
  ```

#### 3. Installing Dependencies Manually

You will need to manually install each of the necessary dependencies. Run the following command to install the dependencies:
```bash
pip install numpy pandas scikit-learn tensorflow streamlit matplotlib seaborn psycopg2
```
Below is a breakdown of the libraries included:

- **`numpy`**: Used for numerical operations and matrix computations.
- **`pandas`**: Essential for data manipulation and handling large datasets.
- **`scikit-learn`**: Required for machine learning algorithms like **K-Means Clustering**.
- **`tensorflow`**: A core dependency for training **Autoencoders**.
- **`streamlit`**: The framework used for creating the project’s frontend dashboard.
- **`matplotlib`** and **`seaborn`**: Used for visualizing data and results.
- **`psycopg2`**: PostgreSQL adapter to allow Python to interact with your PostgreSQL database.

If you encounter any issues with installation or specific dependencies, ensure that your `pip` is up to date:
```bash
pip install --upgrade pip
```
Additionally, for environments with strict dependencies, you may use the following options to bypass caches or force clean installations:
```bash
pip install --no-cache-dir numpy pandas scikit-learn tensorflow streamlit matplotlib seaborn psycopg2
```

### Setting Up PostgreSQL (If Applicable)

#### 1. Install PostgreSQL

If your project includes database interaction (like storing logs or evaluations), you need PostgreSQL installed. On most systems, you can install it via a package manager or from [PostgreSQL’s website](https://www.postgresql.org/download/).

Once installed, verify that the PostgreSQL service is up and running:
```bash
psql -V
```

#### 2. Create a Database

Use the following commands to create a new PostgreSQL database for your project:
```bash
psql -U your_username -c "CREATE DATABASE netguard;"
```
Replace `your_username` with your actual PostgreSQL username. Afterward, verify the database creation:
```bash
psql -U your_username -d netguard
```

#### 3. Set Up Database Tables

To interact with the database, you'll need to create tables. You can execute the following SQL commands in PostgreSQL to create the necessary tables for storing logs and evaluation results:
```sql
CREATE TABLE network_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    source_ip VARCHAR(15) NOT NULL,
    destination_ip VARCHAR(15) NOT NULL,
    protocol VARCHAR(10) NOT NULL,
    data_size INT NOT NULL,
    anomaly BOOLEAN DEFAULT FALSE
);

CREATE TABLE model_evaluations (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(50) NOT NULL,
    precision FLOAT,
    recall FLOAT,
    f1_score FLOAT,
    silhouette_score FLOAT,
    inertia FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
To execute these commands, save them in a `.sql` file and run:
```bash
psql -U your_username -d netguard -f create_tables.sql
```

### Connecting to PostgreSQL Database

Ensure the project’s database connection settings are correctly configured to connect to your PostgreSQL instance. You may need to modify the database credentials in your application’s configuration, such as:
```python
DATABASE_CONFIG = {
    'dbname': 'netguard',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'port': '5432'
}
```

### Troubleshooting Installation Issues

1. **Permission Issues**:
   If you encounter permission issues, especially during database or environment setup, ensure that you have sufficient privileges. On Windows, try running the command prompt or terminal as an administrator.

2. **Environment Activation Errors**:
   If you cannot activate the virtual environment, verify that the execution policy allows it. On Windows, use the following command:
   ```bash
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **PostgreSQL Configuration Errors**:
   If PostgreSQL connections fail, check whether the database service is running and whether your configuration file is properly set up. Look for connection-specific errors in the PostgreSQL logs.

4. **Dependency Conflicts**:
   If you encounter conflicts with package versions, use dependency management tools like `pipenv` or `poetry` for more granular control over package versions and dependencies. You can also manually adjust the versions in `requirements.txt` if available.

### Conclusion

Following these installation steps will set up the **Net Guard** anomaly detection system on your machine. Once dependencies are installed and PostgreSQL is set up (if required), you're ready to proceed with running the project. Should any issues arise during setup, refer to the troubleshooting tips provided above or consult the relevant official documentation for the tools and libraries used in this project.

## Running the Project

### Starting the Streamlit Dashboard

After setting up the environment and installing dependencies, run the following command to start the Streamlit dashboard:

```bash
streamlit run src/Streamlit/app.py
```

This will open a local server in your browser where you can interact with the project, upload datasets, and view the results.

### Uploading Data

In the Streamlit interface, you'll be prompted to upload a dataset (CSV format). The dataset should consist of **network traffic logs**, ideally from the UNSW-NB15 dataset, or any other dataset containing labeled or unlabeled anomalies.

## Evaluation and Metrics

### K-Means Clustering Evaluation

K-Means clustering is evaluated using the following metrics:

1. **Silhouette Score**: Measures how similar each point is to its cluster.
2. **Inertia**: Measures the sum of squared distances from each point to its assigned cluster center.

### Autoencoder Evaluation

The Autoencoder is evaluated based on the following metrics:

1. **Reconstruction Error**: The difference between the input and the reconstructed output. Higher reconstruction error indicates potential anomalies.
2. **Precision**: The ratio of true positive predictions to the total predicted positives.
3. **Recall**: The ratio of true positive predictions to the total actual positives.
4. **F1 Score**: A harmonic mean of precision and recall.

### Data Preprocessing

The preprocessing module handles:

- **Data Scaling**: Normalizes numeric values to a standard range (0-1) for better model performance.
- **Handling Missing Data**: Employs techniques like **KNN imputation** to fill missing values in the dataset.

### Model Training

1. **K-Means Clustering**:
    - The K-Means algorithm clusters the data into a predefined number of clusters.
    - The number of clusters can be set in the Streamlit dashboard.

2. **Autoencoder**:
    - A deep learning Autoencoder model is used to reconstruct input data.
    - Anomalies are detected based on high reconstruction errors.

## Visualization Dashboard

The **Streamlit dashboard** provides a visualization of the evaluation results:

- For K-Means, it visualizes the **Silhouette Score** and **Inertia** metrics.
- For Autoencoders, it displays the **Reconstruction Error Distribution** to show how well the anomalies are being detected.

## Testing and Validation

The system has been tested with the **UNSW-NB15 dataset** to evaluate the model's performance in real-world anomaly detection. You can also provide your own network traffic data to see how the models perform on different datasets.

## Contributing

We welcome contributions! If you have suggestions, bug fixes, or new features, feel free to fork the repository and submit a pull request. Make sure to follow the steps below to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Acknowledgements

- The **UNSW-NB15 dataset** used in this project is publicly available and widely used in network anomaly detection research.
- Thanks to the **Scikit-learn** and **TensorFlow** communities for providing excellent tools for machine learning and anomaly detection.

```
