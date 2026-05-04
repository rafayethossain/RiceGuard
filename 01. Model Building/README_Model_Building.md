# Rice Disease Classification: Model Building Guide

Welcome to the **Rice Disease Classification** project. This guide provides a comprehensive, step-by-step walkthrough to set up your environment, prepare the dataset, and train the deep learning model on your local machine.

---

## 📋 Table of Contents
- [Rice Disease Classification: Model Building Guide](#rice-disease-classification-model-building-guide)
  - [📋 Table of Contents](#-table-of-contents)
  - [🛠 Prerequisites](#-prerequisites)
  - [🚀 Environment Setup](#-environment-setup)
    - [1. Create a Virtual Environment](#1-create-a-virtual-environment)
    - [2. Activate the Environment](#2-activate-the-environment)
    - [3. Install Dependencies](#3-install-dependencies)
  - [📂 Project Configuration](#-project-configuration)
  - [📓 Running the Notebook](#-running-the-notebook)
  - [🔧 Local Path Adjustments](#-local-path-adjustments)
    - [1. Update Extraction Logic](#1-update-extraction-logic)
    - [2. Update Dataset Paths](#2-update-dataset-paths)
  - [🔄 Training Workflow](#-training-workflow)

---

## 🛠 Prerequisites

Before starting, ensure you have the following installed:
*   **Python 3.9+**
*   **pip** (Python package manager)
*   **Jupyter Notebook** or **JupyterLab**

---

## 🚀 Environment Setup

To keep your system clean, it is highly recommended to use a virtual environment.

### 1. Create a Virtual Environment
Navigate to the `01. Model Building` directory in your terminal and run:
```bash
python -m venv venv
```

### 2. Activate the Environment
*   **Windows:**
    ```bash
    .\venv\Scripts\activate
    ```
*   **macOS/Linux:**
    ```bash
    source venv/bin/activate
    ```
### 3. Install Dependencies
With the environment activated, install the necessary libraries:
```bash
pip install -r requirements_app.txt
```

---

## 📂 Project Configuration

Ensure your directory structure looks like this:
```text
01. Model Building/
├── Rice_Disease_Classifier.ipynb
├── plant_small.zip
└── venv/
```
*   **Train Data Source: Google Drive Link:**  [Google Drive Link](https://drive.google.com/file/d/1Rs2UlLooaQuw8ToTTXTlPZ56f-siS3Tc/view?usp=drive_link)
*   
---

## 📓 Running the Notebook

1.  **Launch Jupyter:**
    In your terminal, run:
    ```bash
    jupyter notebook
    ```
2.  **Open the File:**
    In the browser tab that opens, locate and click on `Rice_Disease_Classifier.ipynb`.

---

## 🔧 Local Path Adjustments

The original notebook was designed for **Google Colab**. To run it locally, you must modify the data loading cells.

### 1. Update Extraction Logic
Locate the cell responsible for unzipping the data and replace it with this local-friendly snippet:

```python
import zipfile
import os

# Define local paths
zip_path = 'plant_small.zip'
extract_path = 'plant_data'

# Create directory and extract
if not os.path.exists(extract_path):
    os.makedirs(extract_path)

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)
```

### 2. Update Dataset Paths
Find the cells calling `image_dataset_from_directory` and update the `directory` parameter:

```python
# Training Dataset
train_ds = keras.utils.image_dataset_from_directory(
    directory='plant_data/plant_small/train',
    image_size=(224, 224),
    batch_size=32
)

# Validation Dataset
val_ds = keras.utils.image_dataset_from_directory(
    directory='plant_data/plant_small/val',
    image_size=(224, 224),
    batch_size=32
)
```

---

## 🔄 Training Workflow

Once the paths are set, execute the cells sequentially (**Shift + Enter**) to perform the following:

1.  **Data Preparation:** Load and preprocess the images.
2.  **Visualization:** Inspect sample images from the dataset.
3.  **Model Architecture:** Build the Convolutional Neural Network (CNN).
4.  **Training:** Train the model on the rice leaf dataset.
5.  **Evaluation:** Analyze accuracy and loss curves.
6.  **Interactive Test:** Launch a **Gradio UI** within the notebook to test images manually.
7.  **Export:** Save the trained model as `rice_disease_model.keras` for use in the Web App.

---

> **Tip:** If you encounter "Out of Memory" errors during training, try reducing the `batch_size` to `16`.
