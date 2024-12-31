
---

# Net-Guard: Anomaly Detection in Network Security Logs

Net-Guard is an advanced system for **anomaly detection in network security logs**, leveraging AI techniques like clustering and autoencoders. It uses the **UNSW-NB15 dataset** for training and evaluation, focusing on improving network security by identifying anomalies such as unauthorized access, malware, and unusual traffic patterns.

---

## **Table of Contents**
- [Project Overview](#project-overview)
- [Features](#features)
- [Directory Structure](#directory-structure)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## **Project Overview**

The goal of Net-Guard is to provide a robust, scalable, and efficient system for detecting and visualizing anomalies in network security logs. The project combines data preprocessing, clustering, and visualization to improve the accuracy and interpretability of network intrusion detection.

---

## **Features**

- **Dataset**: Incorporates the UNSW-NB15 dataset for realistic network intrusion detection research.
- **Data Preprocessing**: Handles missing values, encodes categorical data, and normalizes features.
- **AI Models**: Implements clustering (K-Means) and deep learning (autoencoders) for anomaly detection.
- **Visualization Dashboard**: Displays insights into network traffic patterns and detected anomalies.

---

## **Directory Structure**

```
net-guard/
├── data/                      # Dataset directory
│   ├── UNSW_NB15_training-set.csv
│   ├── UNSW_NB15_testing-set.csv
├── notebooks/                 # Jupyter Notebooks for EDA and experimentation
│   ├── 01-exploratory-data-analysis.ipynb
│   ├── 02-data-preprocessing.ipynb
│   ├── 03-clustering-and-anomaly-detection.ipynb
├── src/                       # Source code
│   ├── preprocessing.py       # Scripts for data preprocessing
│   ├── clustering.py          # Clustering models
│   ├── visualization.py       # Visualization scripts
│   ├── anomaly_detection.py   # Main anomaly detection logic
├── results/                   # Results directory (EDA plots, models, reports)
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── main.py                    # Main script to run the pipeline
```

---

## **Setup Instructions**

### **1. Clone the Repository**
Clone the repository to your local machine:
```bash
git clone https://gitlab.com/kidus489/net-guard.git
cd net-guard
```

### **2. Install Dependencies**
Set up a Python virtual environment and install the required dependencies:
```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### **3. Download the Dataset**
Place the **UNSW-NB15 training and testing CSV files** in the `data/` directory:
- [Download UNSW-NB15 Dataset](https://research.unsw.edu.au/projects/unsw-nb15-dataset)

### **4. Run Jupyter Notebooks (Optional)**
For exploratory data analysis and experimentation:
```bash
jupyter notebook
```
Navigate to the `notebooks/` directory to open a specific notebook.

### **5. Run the Pipeline**
Execute the main script to process the data and run the anomaly detection pipeline:
```bash
python main.py
```

---

## **Usage**

### **Dataset Preprocessing**
Run the `preprocessing.py` script to clean and prepare the dataset:
```bash
python src/preprocessing.py
```

### **Clustering Models**
Use the `clustering.py` script to apply clustering algorithms:
```bash
python src/clustering.py
```

### **Visualization**
Generate anomaly visualizations using `visualization.py`:
```bash
python src/visualization.py
```

---

## **Contributing**

We welcome contributions from all team members! Follow these steps:

1. **Fork the Repository**: Create a personal copy on your GitLab account.
2. **Create a Branch**: Work on a new feature or bug fix.
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. **Commit Changes**: Write meaningful commit messages.
    ```bash
    git commit -m "Add feature: your feature description"
    ```
4. **Push Changes**: Push your branch to the repository.
    ```bash
    git push origin feature/your-feature-name
    ```
5. **Create a Merge Request**: Submit a merge request on GitLab for review.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

---

