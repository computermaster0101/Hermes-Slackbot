import os
import json

import subprocess
import threading
import time

from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
from routes import init_routes  # Import the function to initialize routes
from rule_set import RuleSet  # Import RuleSet
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Load environment variables from .env
load_dotenv()
HOST = os.getenv('HOST', 'localhost')
PORT = os.getenv('PORT', 5000)
SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
RULES_DIR = os.getenv('RULESDIR', './rules/win10')  # Path to the rules directory

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)

# Initialize the RuleSet object
rules = RuleSet(RULES_DIR)

# Initialize routes
init_routes(app, rules, socketio)

class RulesDirectoryHandler(FileSystemEventHandler):
    """Handler for monitoring the rules directory and recreating the RuleSet on changes."""
    def on_any_event(self, event):
        if event.event_type in ['modified', 'created']:  # Handle only specific events
            global rules
            # Recreate the RuleSet whenever a file is created, modified, deleted, or moved after a short delay
            print("Change detected in rules directory. Reloading rules...")
            rules = None  # Optional: Clears any references
            rules = RuleSet(RULES_DIR)
            rules_data = {file: str(rule) for file, rule in rules.rules.items()}
            socketio.emit('rules_updated', json.dumps(rules_data))
            #socketio.emit('rules_updated', {file: str(rule) for file, rule in rules.rules.items()})
            

def watch_rules_directory():
    """Watch the rules directory for any changes and update the RuleSet accordingly."""
    event_handler = RulesDirectoryHandler()
    observer = Observer()
    observer.schedule(event_handler, RULES_DIR, recursive=False)
    observer.start()

    try:
        while True:
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def run_main():
    """Function to run the main message processing logic."""
    process = subprocess.Popen(['python', 'main.py'])
    process.wait()  # Wait for the subprocess to complete
    os._exit(0)

if __name__ == '__main__':
    # Start the main processing logic in a separate thread
    main_thread = threading.Thread(target=run_main)
    main_thread.start()

    # Start a thread to watch the rules directory for changes
    watch_thread = threading.Thread(target=watch_rules_directory)
    watch_thread.daemon = True
    watch_thread.start()

    # Start the Flask-SocketIO server
    print(f'Starting on {HOST}:{PORT}')
    socketio.run(app, host=HOST, port=PORT)

    # Wait for the main thread to finish
    main_thread.join()

    # Stop the server gracefully if the main thread ends
    socketio.stop()
