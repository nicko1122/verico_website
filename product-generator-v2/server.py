import os
import sys
import logging
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from processor_v2 import process_zip_v2, INBOX_DIR, FAILED_DIR  # type: ignore


# --- Flask App Initialization ---
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))


# --- Basic Setup & Configuration ---
load_dotenv()
LOG_FILE = os.path.join(os.path.dirname(__file__), 'server.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

app.config['UPLOAD_FOLDER'] = INBOX_DIR
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # 64 MB limit


# --- Ensure Directories Exist ---
for p in [INBOX_DIR, FAILED_DIR]:
    os.makedirs(p, exist_ok=True)
    logging.info(f"Ensured directory exists: {p}")


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'zip'


# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part in the request."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({"message": "Invalid file type. Please upload a .zip file."}), 400

    filename = secure_filename(file.filename)
    zip_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        file.save(zip_path)
        logging.info(f"Saved upload to {zip_path}")
        product_url = process_zip_v2(zip_path)
        logging.info(f"Processed successfully. URL: {product_url}")
        return jsonify({
            "message": "Product processed successfully!",
            "product_url": product_url
        }), 200
    except Exception as e:
        logging.exception(f"Processing failed for {filename}: {e}")
        return jsonify({"message": f"An error occurred: {e}"}), 500


if __name__ == '__main__':
    # Optional: verify API key presence for clarity (processor uses OpenAI SDK under the hood)
    if not os.getenv('OPENAI_API_KEY'):
        logging.warning('OPENAI_API_KEY is not set. LLM translation will fail.')
    app.run(host='0.0.0.0', port=5011, debug=False)


