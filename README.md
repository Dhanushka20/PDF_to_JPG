# PDF to JPG Converter

This is a simple web application that allows users to convert PDF files to JPG images. Users can either convert entire pages into images or extract embedded images from a PDF file.

## Features
- Convert PDF pages to JPG images
- Extract images from PDF files
- User-friendly drag-and-drop file upload
- Built with Flask for backend processing
- Uses TailwindCSS for a clean and modern UI

## Installation
### Prerequisites
Ensure you have Python installed on your system. You also need `pip` for package management.

### Clone the Repository
```bash
git clone https://github.com/yourusername/pdf-to-jpg-converter.git
cd pdf-to-jpg-converter
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application
```bash
python app.py
```
The application will run locally on `http://127.0.0.1:5000/`.

## Usage
1. Open the application in your browser.
2. Drag and drop a PDF file or click to browse.
3. Choose a conversion option:
   - Convert Pages to JPG
   - Extract Images
4. Click on the "Convert PDF" button.
5. Download the converted images in a ZIP file.

## Project Structure
```
├── static
│   ├── script.js  # JavaScript for frontend interactions
│   ├── style.css  # Custom styles (if any)
├── templates
│   ├── index.html  # Main frontend page
├── app.py  # Flask backend application
├── requirements.txt  # Dependencies
├── README.md  # Project documentation
```

## Dependencies
- Flask
- PyMuPDF (fitz)
- Pillow

Install these dependencies using:
```bash
pip install Flask fitz Pillow
```

## License
This project is licensed under the MIT License.

## Author
Dhanushka

