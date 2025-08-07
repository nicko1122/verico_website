import sys
import time
import logging
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from processor import process_zip, WATCH_PATH, FAILED_PATH
from dotenv import load_dotenv
import openai

# --- Basic Setup ---
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
LOG_FILE = os.path.join(os.path.dirname(__file__), 'watcher.log')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[
                        logging.FileHandler(LOG_FILE),
                        logging.StreamHandler()
                    ])

class NewProductHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith('.zip'):
            return
        
        # Wait for the file to be fully written to avoid processing partial files
        time.sleep(2)
        
        logging.info(f"New zip file detected by watcher: {os.path.basename(event.src_path)}")
        try:
            process_zip(event.src_path)
        except Exception as e:
            # The error is already logged in process_zip, so we just pass here
            pass

def start_watcher():
    # Ensure necessary directories exist
    for p in [WATCH_PATH, FAILED_PATH]:
        if not os.path.exists(p):
            os.makedirs(p)
            logging.info(f"Created directory: {p}")

    observer = Observer()
    event_handler = NewProductHandler()
    observer.schedule(event_handler, WATCH_PATH, recursive=False)
    
    logging.info(f"Starting file watcher for directory: {WATCH_PATH}")
    logging.info("Press Ctrl+C to stop.")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Watcher stopped by user.")
    
    observer.join()

if __name__ == "__main__":
    if not openai.api_key:
        logging.error("OPENAI_API_KEY environment variable not set. Please create a .env file.")
        sys.exit(1)
    start_watcher()
