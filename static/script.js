const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');
const dropZone = document.getElementById('dropZone');
const convertButton = document.getElementById('convertButton');
const form = document.getElementById('convertForm');
const errorDiv = document.getElementById('error');
const successDiv = document.getElementById('success');

dropZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
    if (e.target.files[0]) {
        fileName.textContent = e.target.files[0].name;
        dropZone.classList.add('border-indigo-500');
    }
});

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
    });
});

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => {
        dropZone.classList.add('border-indigo-500', 'bg-gray-50');
    });
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => {
        dropZone.classList.remove('border-indigo-500', 'bg-gray-50');
    });
});

dropZone.addEventListener('drop', (e) => {
    fileInput.files = e.dataTransfer.files;
    if (e.dataTransfer.files[0]) {
        fileName.textContent = e.dataTransfer.files[0].name;
    }
});

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorDiv.style.display = 'none';
    successDiv.style.display = 'none';
    convertButton.disabled = true;
    
    const loadingSpinner = `
        <svg class="inline-block animate-spin h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Converting...
    `;
    convertButton.innerHTML = loadingSpinner;
    
    try {
        const formData = new FormData(form);
        const response = await fetch('/convert', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'converted_images.zip';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            successDiv.textContent = 'Conversion successful! Downloading...';
            successDiv.style.display = 'block';
        } else {
            const error = await response.text();
            throw new Error(error);
        }
    } catch (error) {
        errorDiv.textContent = `Error: ${error.message}`;
        errorDiv.style.display = 'block';
    } finally {
        convertButton.disabled = false;
        convertButton.innerHTML = 'Convert PDF';
    }
});