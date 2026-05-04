# 🌾 RiceGuard AI: Local Launch Guide

Welcome to the **Rice Leaf Disease Diagnosis Platform**. This guide will help you deploy the RiceGuard AI web application locally, allowing you to use your trained deep learning model to diagnose rice diseases with high precision and visual explanations.

---

## 📋 Table of Contents
1. [System Requirements](#-system-requirements)
2. [Environment Setup](#-environment-setup)
3. [Launching the Application](#-launching-the-application)
4. [User Guide: Testing the AI](#-user-guide-testing-the-ai)
5. [File Structure Checklist](#-file-structure-checklist)
6. [Troubleshooting](#-troubleshooting)

---

## 💻 System Requirements

*   **Python:** Version 3.10 or newer.
*   **Assets:** Ensure your trained `rice_disease_model.keras` and `class_names.json` are present in the `02. Web App/` directory.

---

## 🚀 Environment Setup

Follow these steps to prepare your local environment for the application.

### 1. Create a Virtual Environment
Open your terminal in the `02. Web App/` directory and run:
```bash
python -m venv app_env
```

### 2. Activate the Environment
*   **Windows:**
    ```bash
    .\app_env\Scripts\activate
    ```
*   **macOS/Linux:**
    ```bash
    source app_env/bin/activate
    ```

### 3. Install Dependencies
```bash
pip install -r requirements_app.txt
```

---

## 🛠 Launching the Application

The platform consists of a **FastAPI backend** (the brain) and a **web frontend** (the interface).

### Step 1: Start the Backend (API)
Run the following command to start the diagnosis engine:
```bash
python -m uvicorn app:app --reload
```
> **Success Check:** You should see `INFO: Uvicorn running on http://127.0.0.1:8000`. Keep this terminal window open.

### Step 2: Open the Frontend
1. Navigate to the `02. Web App/` folder in your File Explorer.
2. **Double-click `index.html`** to open it in your preferred web browser.
3. You will be greeted by the **Glassmorphism UI**.

---

## 🔍 User Guide: Testing the AI

1.  **Upload Image:** Drag an image from your `test_image/` folder or click to upload a rice leaf photo.
2.  **Initialize:** Click the **"Initialize Diagnosis"** button.
3.  **Review Results:**
    *   **Diagnosis:** See the predicted disease and the confidence percentage.
    *   **XAI Heatmap:** The AI generates a heatmap showing exactly which parts of the leaf influenced the diagnosis.
    *   **Treatment Plan:** View specific remedial actions for the detected disease.

---

## 📂 File Structure Checklist

For the application to function correctly, ensure the following files are in the same directory:
*   `app.py` — The FastAPI backend logic.
*   `index.html` — The main user interface.
*   `style.css` — Visual styling and layout.
*   `script.js` — Client-side logic and API communication.
*   `rice_disease_model.keras` — The trained CNN model.
*   `class_names.json` — The mapping of model outputs to disease names.

---

## ❓ Troubleshooting

| Issue | Potential Solution |
| :--- | :--- |
| **Diagnosis Failed Error** | Ensure the FastAPI server is still running in your terminal. |
| **ModuleNotFoundError** | Re-run `pip install -r requirements_app.txt` with your environment activated. |
| **Model Load Error** | Verify that `rice_disease_model.keras` is in the correct folder and not corrupted. |
| **No UI Displayed** | Refresh `index.html` or try opening it in a modern browser (Chrome, Edge, or Firefox). |

---
*Developed for the Bangladesh Ship Recycling Industry & Agricultural Sector.*
