const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const diagnoseBtn = document.getElementById('diagnose-btn');
const resultsSection = document.getElementById('results-section');
const loader = document.getElementById('loader');
const previewContainer = document.getElementById('preview-container');
const uploadContent = document.querySelector('.upload-content');
const imagePreview = document.getElementById('image-preview');
const cancelBtn = document.getElementById('cancel-btn');

let selectedFile = null;

// Task 4.1 Integration Fix: Ensure the API URL matches the FastAPI server exactly
const API_URL = 'http://127.0.0.1:8000/predict';

// Drag & Drop event listeners
dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('active'); });
dropZone.addEventListener('dragleave', () => { dropZone.classList.remove('active'); });
dropZone.addEventListener('drop', (e) => { e.preventDefault(); dropZone.classList.remove('active'); handleFile(e.dataTransfer.files[0]); });
dropZone.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', (e) => handleFile(e.target.files[0]));

function handleFile(file) {
    if (file && file.type.startsWith('image/')) {
        selectedFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            previewContainer.classList.remove('hidden');
            uploadContent.classList.add('hidden');
            diagnoseBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    } else {
        alert("Please upload a valid image file.");
    }
}

cancelBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    selectedFile = null;
    previewContainer.classList.add('hidden');
    uploadContent.classList.remove('hidden');
    diagnoseBtn.disabled = true;
    fileInput.value = '';
    resultsSection.classList.add('hidden');
});

// Primary Diagnosis Logic
diagnoseBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    // Show scanning animation
    loader.classList.remove('hidden');
    resultsSection.classList.add('hidden');
    diagnoseBtn.disabled = true;

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        console.log("Sending diagnosis request to:", API_URL);
        const response = await fetch(API_URL, { 
            method: 'POST', 
            body: formData,
            mode: 'cors' // Ensure CORS mode is explicitly enabled
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Diagnosis Failed');
        }

        const data = await response.json();
        console.log("Diagnosis Data Received:", data);
        displayResults(data);
    } catch (error) {
        console.error("Integration Error:", error);
        alert('Diagnosis Hub Offline or Error: ' + error.message);
    } finally {
        loader.classList.add('hidden');
        diagnoseBtn.disabled = false;
    }
});

function displayResults(data) {
    resultsSection.classList.remove('hidden');
    
    // Result Label & Confidence
    document.getElementById('result-label').innerText = data.prediction;
    const confidencePercent = (data.confidence * 100).toFixed(1);
    document.getElementById('confidence-text').innerText = confidencePercent + '% Confidence';
    document.getElementById('confidence-bar').style.width = confidencePercent + '%';

    // XAI Heatmap Render
    const heatmapImg = document.getElementById('heatmap-img');
    heatmapImg.src = `data:image/jpeg;base64,${data.heatmap}`;

    // Treatment Data Render
    document.getElementById('treatment-desc').innerText = data.treatment.description;
    const stepsList = document.getElementById('treatment-steps');
    stepsList.innerHTML = '';
    data.treatment.steps.forEach(step => {
        const li = document.createElement('li');
        li.innerText = step;
        stepsList.appendChild(li);
    });

    // Top Probability Distribution List
    const list = document.getElementById('prediction-list');
    list.innerHTML = '';
    data.top_3.forEach(item => {
        const div = document.createElement('div');
        div.className = 'prediction-item';
        div.innerHTML = `<span>${item.label}</span><span>${(item.confidence * 100).toFixed(1)}%</span>`;
        list.appendChild(div);
    });

    // Smooth scroll to analysis
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}
