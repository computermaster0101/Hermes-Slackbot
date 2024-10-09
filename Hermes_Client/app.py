import os
import json
import subprocess
import threading
from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
from sockets import init_routes
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Specify the paths for the environment files
custom_env_path = os.path.expanduser('~/hermes.env')
default_env_path = '.env'

# Load the custom .env file if it exists; otherwise, load the default .env
if os.path.exists(custom_env_path):
    load_dotenv(custom_env_path)
    print(f"Loaded environment variables from {custom_env_path}")
else:
    load_dotenv(default_env_path)
    print(f"Loaded environment variables from {default_env_path}")

HOST = os.getenv('HOST', 'localhost')
PORT = os.getenv('PORT', 5000)
SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)

init_routes(app, socketio)

def run_main():
    process = subprocess.Popen(['python', 'main.py'])
    process.wait()
    os._exit(0)

if __name__ == '__main__':
    main_thread = threading.Thread(target=run_main)
    main_thread.start()
    print(f'Starting on {HOST}:{PORT}')
    socketio.run(app, host=HOST, port=PORT)
    main_thread.join()
    socketio.stop()
