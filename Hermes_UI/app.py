import os
import json
import subprocess
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from dotenv import load_dotenv
import threading
from rule_set import RuleSet  # Import RuleSet

# Load environment variables from .env
load_dotenv()
HOST = os.getenv('HOST', 'localhost')
PORT = int(os.getenv('PORT', 5000))
SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')  # Set a default if not in .env
RULES_DIR = os.getenv('RULESDIR', './rules/win10')  # Path to the rules directory

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)

# Initialize the RuleSet object
rules = RuleSet(RULES_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rules', methods=['GET'])
def get_rules():
    """Fetch the rules as a JSON response."""
    rules_data = {file: str(rule) for file, rule in rules.rules.items()}
    return jsonify(rules_data)

def run_main():
    """Function to run the main message processing logic."""
    # Start main.py as a subprocess
    process = subprocess.Popen(['python', 'main.py'])
    process.wait()  # Wait for the subprocess to complete
    # If main.py exits, exit the parent process
    os._exit(0)

if __name__ == '__main__':
    # Start the main processing logic in a separate thread
    main_thread = threading.Thread(target=run_main)
    main_thread.start()

    # Start the Flask-SocketIO server
    print(f'Starting on {HOST}:{PORT}')
    socketio.run(app, host=HOST, port=PORT)

    # Wait for the main thread to finish
    main_thread.join()

    # Stop the server gracefully if the main thread ends
    socketio.stop()
