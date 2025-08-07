import os
import sys
import logging
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from processor import process_zip, WATCH_PATH, FAILED_PATH
from dotenv import load_dotenv
import openai

# --- Flask App Initialization ---
app = Flask(__name__)

# --- Basic Setup & Configuration ---
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
LOG_FILE = os.path.join(os.path.dirname(__file__), 'server.log')

# Configure logging for the server
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[
                        logging.FileHandler(LOG_FILE),
                        logging.StreamHandler()
                    ])

app.config['UPLOAD_FOLDER'] = WATCH_PATH
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# --- Ensure Directories Exist ---
for p in [WATCH_PATH, FAILED_PATH]:
    if not os.path.exists(p):
        os.makedirs(p)
        logging.info(f"Created directory: {p}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'zip'

# --- Routes ---
@app.route('/')
def index():
    """Renders the main upload page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles the file upload and processing."""
    if 'file' not in request.files:
        return jsonify({"message": "No file part in the request."}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"message": "No file selected."}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        zip_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            file.save(zip_path)
            logging.info(f"File {filename} saved to {zip_path}")
            
            # Directly call the processing function
            product_url = process_zip(zip_path)
            
            logging.info(f"Successfully processed {filename}. Product URL: {product_url}")
            return jsonify({
                "message": "Product processed successfully!",
                "product_url": product_url
            }), 200

        except Exception as e:
            # The processor already logs the detailed error and moves the file
            logging.error(f"Caught exception while processing {filename}: {e}")
            return jsonify({"message": f"An error occurred: {e}"}), 500
            
    else:
        return jsonify({"message": "Invalid file type. Please upload a .zip file."}), 400

# --- Main Execution ---
if __name__ == '__main__':
    if not openai.api_key:
        logging.error("FATAL: OPENAI_API_KEY environment variable not set.")
        sys.exit(1)
    # Use host='0.0.0.0' to make it accessible from the network
    app.run(host='0.0.0.0', port=5001, debug=True)

