from flask import Flask, render_template, request, send_file
import fitz
from PIL import Image
import os
import shutil
import io
import uuid
from pathlib import Path

app = Flask(__name__, static_folder='static', template_folder='templates')

UPLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'pdf_converter_uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf_file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['pdf_file']
    if file.filename == '':
        return 'No file selected', 400
    
    if not allowed_file(file.filename):
        return 'Invalid file type', 400
    
    try:
        conversion_type = request.form.get('conversion_type', 'pages')
        unique_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()))
        os.makedirs(unique_dir, exist_ok=True)
        
        try:
            # Save and process PDF
            pdf_path = os.path.join(unique_dir, f"{str(uuid.uuid4())}.pdf")
            file.save(pdf_path)
            memory_file = io.BytesIO()
            doc = fitz.open(pdf_path)
            
            if conversion_type == 'pages':
                # Convert pages to JPG
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    pix = page.get_pixmap()
                    img_data = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    img_path = os.path.join(unique_dir, f'page_{page_num + 1}.jpg')
                    img_data.save(img_path, 'JPEG', quality=90)
            else:
                # Extract images
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    image_list = page.get_images()
                    for img_idx, img in enumerate(image_list):
                        xref = img[0]
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        img_data = Image.open(io.BytesIO(image_bytes))
                        img_path = os.path.join(unique_dir, f'image_{page_num + 1}_{img_idx + 1}.jpg')
                        img_data.save(img_path, 'JPEG', quality=90)
            
            doc.close()
            
            # Create ZIP file
            from zipfile import ZipFile
            with ZipFile(memory_file, 'w') as zf:
                for img_file in Path(unique_dir).glob('*.jpg'):
                    zf.write(img_file, img_file.name)
            
            memory_file.seek(0)
            
            return send_file(
                memory_file,
                mimetype='application/zip',
                as_attachment=True,
                download_name='converted_images.zip'
            )
            
        finally:
            if os.path.exists(unique_dir):
                shutil.rmtree(unique_dir, ignore_errors=True)
                
    except Exception as e:
        return f"Error processing file: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)