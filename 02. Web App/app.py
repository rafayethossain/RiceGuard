from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import io
import json
import base64
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="RiceGuard AI | Fixed XAI Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model
MODEL_PATH = 'rice_disease_model.keras'
CLASS_NAMES_PATH = 'class_names.json'

try:
    # Explicitly load with custom objects if any, though standard .keras should be fine
    model = tf.keras.models.load_model(MODEL_PATH)
    with open(CLASS_NAMES_PATH, 'r') as f:
        class_names = json.load(f)
    logger.info(f"Model loaded. Classes: {class_names}")
except Exception as e:
    logger.error(f"Load Error: {e}")
    model = None
    class_names = []

TREATMENTS = {
    "Bacterial Leaf Blight": {
        "description": "Bacterial infection causing yellowing and drying of leaves.",
        "steps": ["Apply copper-based fungicides", "Reduce nitrogen fertilizer", "Ensure proper field drainage"]
    },
    "Brown Spot": {
        "description": "Fungal disease linked to nutrient-deficient soil.",
        "steps": ["Apply potassium fertilizer", "Use fungicides like Mancozeb", "Improve soil quality"]
    },
    "Healthy Rice Leaf": {
        "description": "The leaf shows no signs of disease.",
        "steps": ["Continue regular monitoring", "Maintain balanced irrigation", "Ensure proper sunlight"]
    },
    "Leaf Blast": {
        "description": "Serious fungal infection causing spindle-shaped spots.",
        "steps": ["Avoid excessive nitrogen", "Apply Tricyclazole fungicides", "Remove infected crop residue"]
    },
    "Leaf scald": {
        "description": "Fungal disease starting from leaf tips/edges.",
        "steps": ["Use resistant varieties", "Apply Benomyl or Carbendazim", "Ensure optimal plant spacing"]
    },
    "Sheath Blight": {
        "description": "Fungal disease affecting the lower parts of the plant.",
        "steps": ["Apply Validamycin", "Increase plant spacing for airflow", "Remove weeds from the field"]
    }
}

def get_gradcam_heatmap(img_array, model):
    try:
        # 1. Identify the EfficientNet layer and the final prediction layer
        base_layer = None
        for layer in model.layers:
            if 'efficientnet' in layer.name.lower():
                base_layer = layer
                break
        
        if not base_layer:
            return np.zeros((7, 7))

        # 2. Find the last convolutional layer inside EfficientNet
        last_conv_layer = None
        for layer in reversed(base_layer.layers):
            if isinstance(layer, tf.keras.layers.Conv2D):
                last_conv_layer = layer
                break
        
        if not last_conv_layer:
            return np.zeros((7, 7))

        # 3. Create a functional sub-model to extract internal features and final prediction
        # This bypasses the Sequential container issues
        conv_output = base_layer.get_layer(last_conv_layer.name).output
        
        # We build a temporary model that goes from EfficientNet input to the internal Conv layer
        # Then we use the top-level Sequential model for the final prediction
        grad_model = tf.keras.models.Model(
            inputs=[model.inputs],
            outputs=[base_layer.get_layer(last_conv_layer.name).output, model.output]
        )

        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_array)
            loss = predictions[:, np.argmax(predictions[0])]

        # Extract gradients
        grads = tape.gradient(loss, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

        # Weight the channels
        conv_outputs = conv_outputs[0]
        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)

        # Normalize
        heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-10)
        return heatmap.numpy()
    except Exception as e:
        logger.error(f"Grad-CAM Failed: {e}")
        return np.zeros((7, 7))

def apply_heatmap(heatmap, original_img):
    heatmap = cv2.resize(heatmap, (original_img.shape[1], original_img.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    superimposed_img = heatmap * 0.4 + original_img
    superimposed_img = np.clip(superimposed_img, 0, 255).astype(np.uint8)
    _, buffer = cv2.imencode('.jpg', cv2.cvtColor(superimposed_img, cv2.COLOR_RGB2BGR))
    return base64.b64encode(buffer).decode('utf-8')

@app.get("/")
async def root():
    return {"status": "online", "model": "EfficientNetV2B0-Rice"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not model: raise HTTPException(status_code=500, detail="Model Not Loaded")
    
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        original_img = np.array(image.resize((400, 400)))
        
        # Preprocess
        img_array = np.array(image.resize((224, 224)))
        img_array = np.expand_dims(img_array, axis=0)
        
        # Predict
        preds = model.predict(img_array)
        class_idx = np.argmax(preds[0])
        label = class_names[class_idx]
        confidence = float(preds[0][class_idx])
        
        # Generate Heatmap
        heatmap = get_gradcam_heatmap(img_array, model)
        heatmap_base64 = apply_heatmap(heatmap, original_img)
        
        treatment = TREATMENTS.get(label, {"description": "N/A", "steps": []})
        
        return {
            "prediction": label,
            "confidence": confidence,
            "top_3": [{"label": class_names[idx], "confidence": float(preds[0][idx])} for idx in np.argsort(preds[0])[-3:][::-1]],
            "heatmap": heatmap_base64,
            "treatment": treatment
        }
    except Exception as e:
        logger.error(f"Prediction Failure: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
