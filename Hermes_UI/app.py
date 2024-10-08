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

load_dotenv()
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
