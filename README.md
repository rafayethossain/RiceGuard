# 🌾 RiceGuard AI: End-to-End Disease Classification & Diagnosis

Welcome to **RiceGuard AI**, a comprehensive deep learning solution designed to identify and diagnose rice leaf diseases. This project covers the entire lifecycle—from training a high-precision CNN model to deploying an interactive Web Application with Explainable AI (XAI) visualizations.

---

## 📋 Project Overview
RiceGuard AI is divided into two main phases:
1.  **Phase 1: Model Building** – Training the CNN model using TensorFlow/Keras.
2.  **Phase 2: Web Application** – A FastAPI-powered dashboard for real-time diagnosis and treatment advice.

---

## 🛠 Prerequisites
*   **Python:** 3.10+ recommended.
*   **Tools:** Pip, Virtual Environment (`venv`), Jupyter Notebook (VS Code).
*   **Hardware:** 8GB+ RAM (Recommended for training).
*   **Train Data Source: Google Drive Link:**  [Google Drive Link](https://drive.google.com/file/d/1Rs2UlLooaQuw8ToTTXTlPZ56f-siS3Tc/view?usp=drive_link)


   

---

## 📂 Project Structure
```text
RiceGuard/
├── 01. Model Building/       # Training environment
│   ├── Rice_Disease_Classifier.ipynb
│   ├── plant_small.zip       # Dataset
│   └── requirements_app.txt  # Training dependencies
└── 02. Web App/              # Deployment environment
    ├── app.py                # FastAPI Backend
    ├── index.html            # Web Frontend
    ├── rice_disease_model.keras # Trained Model
    └── class_names.json      # Mapping labels
```

---

## 🚀 Phase 1: Model Building & Training

Goal: Train the model and export it for the web application.

1.  **Navigate to Directory:**
    ```bash
    cd "01. Model Building"
    ```
2.  **Setup Environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    source venv/bin/activate # macOS/Linux
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements_app.txt
    ```
4.  **Run the Notebook:**
    *   Launch `jupyter notebook` and open `Rice_Disease_Classifier.ipynb`.
    *   **Crucial:** Update the extraction and dataset paths in the notebook as per the local instructions in the notebook's README.
    *   Execute all cells to train and export the model as `rice_disease_model.keras`.

---

## 🌐 Phase 2: Web App Deployment

Goal: Run the interactive diagnosis platform.

1.  **Prepare Assets:**
    Ensure `rice_disease_model.keras` and `class_names.json` are copied/present in the `02. Web App/` directory.
2.  **Navigate to Directory:**
    ```bash
    cd "../02. Web App"
    ```
3.  **Setup Environment:**
    ```bash
    python -m venv app_env
    .\app_env\Scripts\activate  # Windows
    source app_env/bin/activate # macOS/Linux
    ```
4.  **Install Requirements:**
    ```bash
    pip install -r requirements_app.txt
    ```
5.  **Start the Engine (Backend):**
    ```bash
    python -m uvicorn app:app --reload
    ```
6.  **Launch the Interface (Frontend):**
    *   Open `index.html` in your browser to access the **RiceGuard AI Dashboard**.

---

## 🔍 How to Use the Platform
1.  **Upload:** Drag a rice leaf image into the upload zone.
2.  **Diagnose:** Click **"Initialize Diagnosis"**.
3.  **Insights:**
    *   **Accuracy:** View the model's confidence score.
    *   **XAI Heatmap:** See the "glowing" areas on the leaf where the AI detected the disease.
    *   **Treatment:** Follow the generated steps to manage the disease.

---

## ❓ Troubleshooting & Support
*   **Backend Connection:** Ensure the Uvicorn server is running on `http://127.0.0.1:8000`.
*   **Memory Issues:** If training crashes, reduce the `batch_size` to 16 in the Jupyter Notebook.
*   **Missing Files:** Verify the `File Structure Checklist` in the respective phase's README.

---
*Developed for the agricultural Sector.*
