import os
import json
import time
import threading
from rule_set import RuleSet
from message_processor import MessageProcessor
from message import Message
from dotenv import load_dotenv
from flask import render_template, jsonify
from flask_socketio import emit
from threading import Lock

load_dotenv()
DEVICE = os.getenv('SYSNAME', 'missingName')
RULES_DIR = os.getenv('RULESDIR', './rules/win10')
HIST_DIR = os.getenv('HISTDIR', './history')

# Lock for thread-safe file access
lock = Lock()

# Function to save device info to JSON
def save_device_info(heartbeat_interval):
    devices_dir = './devices'
    device_file_path = os.path.join(devices_dir, f"{DEVICE}.json")

    # Initialize device_info with default values
    device_info = {
        "SYSNAME": DEVICE,
        "KEYWORD": os.getenv('KEYWORD', ''),
        "APPDIR": os.getenv('APPDIR', './'),
        "MSGDIR": os.getenv('MSGDIR', './messages'),
        "RULESDIR": os.getenv('RULESDIR', './rules/win10'),
        "HISTDIR": os.getenv('HISTDIR', './history'),
        "SLACK_TOKENx": os.getenv('SLACK_TOKENx', ''),
        "DEFAULT_SLACK_CHANNEL": os.getenv('DEFAULT_SLACK_CHANNEL', ''),
        "Last Updated": time.strftime('%Y-%m-%d %H:%M:%S'),  # Update every time
        "Heartbeat": heartbeat_interval
    }

    # If the file exists, don't update Last Startup
    if os.path.exists(device_file_path):
        with lock:  # Ensure thread-safe access
            # Load existing data to keep Last Startup intact
            with open(device_file_path, 'r') as f:
                existing_info = json.load(f)
                device_info["Last Startup"] = existing_info.get("Last Startup", time.strftime('%Y-%m-%d %H:%M:%S'))
    else:
        # If file doesn't exist, set Last Startup to the current time
        device_info["Last Startup"] = time.strftime('%Y-%m-%d %H:%M:%S')

    # Create directory if it doesn't exist
    os.makedirs(devices_dir, exist_ok=True)

    # Write the device info to the JSON file
    with lock:  # Ensure thread-safe access
        with open(device_file_path, 'w') as f:
            json.dump(device_info, f, indent=4)

# Check for existing device file at startup
def load_device_info():
    device_file_path = os.path.join('./devices', f"{DEVICE}.json")
    
    if os.path.exists(device_file_path):
        with open(device_file_path, 'r') as f:
            return json.load(f)
    else:
        # If file doesn't exist, create one with heartbeat interval
        heartbeat_interval = 300  # Default to 5 minutes (300 seconds)
        save_device_info(heartbeat_interval)
        return {
            "Heartbeat": heartbeat_interval,
            "Last Startup": time.strftime('%Y-%m-%d %H:%M:%S'),
            "Last Updated": time.strftime('%Y-%m-%d %H:%M:%S')
        }  # Return a new dictionary with initial values

# Initialize rules and message processor
rules = RuleSet(RULES_DIR)
message_processor = MessageProcessor(rules)

# Load device info at startup
device_info = load_device_info()

def init_routes(app, socketio):
    @app.route('/')
    def index():
        return render_template('index.html')

    @socketio.on('send_message')
    def send_message(message):
        try:
            get_rule_set()
            message_instance = Message(
                message_text=message.get('text'),
                message_file=None,
                device=DEVICE
            )

            output = message_processor.process_message(message_instance, rules)
            output_string = "\n".join(output)

            history_file = os.path.join(HIST_DIR, f"{time.strftime('%Y%m%d-%H%M%S')}_{DEVICE}.txt")
            os.makedirs(os.path.dirname(history_file), exist_ok=True)

            with open(history_file, "w") as f:
                f.write(f"{message_instance}\n{output_string}")

            socketio.emit('message_response', {'status': 'success', 'output': output_string})

        except Exception as e:
            socketio.emit('message_response', {'status': 'error', 'message': str(e)})

    @socketio.on('get_rule_set')
    def get_rule_set():
        global rules
        rules = RuleSet(RULES_DIR)

        rule_set_data = {
            'rules': {}
        }

        for filename, rule in rules.rules.items():
            rule_set_data['rules'][filename] = {
                'name': rule.name,
                'patterns': rule.patterns,
                'actions': rule.actions,
                'active': rule.active,
                'runningDirectory': rule.runningDirectory,
                'passMessage': rule.passMessage
            }

        socketio.emit('new_rule_set', rule_set_data)

    @socketio.on('request_rule')
    def request_rule(file_name):
        global rules
        rule = rules.rules.get(file_name)

        if rule:
            rule_details = {
                'name': rule.name,
                'patterns': rule.patterns,
                'actions': rule.actions,
                'active': rule.active,
                'runningDirectory': rule.runningDirectory,
                'passMessage': rule.passMessage
            }
            socketio.emit('receive_rule', rule_details)

    @socketio.on('get_devices')
    def get_devices():
        devices_data = []
        devices_dir = './devices'
        
        try:
            for filename in os.listdir(devices_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(devices_dir, filename)
                    with open(file_path, 'r') as f:
                        device_info = json.load(f)
                        devices_data.append({
                            'filename': filename,
                            'device_info': device_info
                        })
            socketio.emit('updated_devices', devices_data)
        except Exception as e:
            socketio.emit('updated_devices', {'error': str(e)})

    @socketio.on('get_history')
    def get_history():
        history_data = []
        history_dir = os.getenv('HISTDIR', './history')
        try:
            for filename in os.listdir(history_dir):
                if filename.endswith('.txt'):
                    file_path = os.path.join(history_dir, filename)
                    with open(file_path, 'r') as f:
                        content = f.read()
                        try:
                            message_data = json.loads(content.splitlines()[0])
                            timestamp = message_data.get('timestamp', 'N/A')
                            status = message_data.get('status', 'N/A')
                            processing_results = content.splitlines()[1:]
                            history_data.append({
                                'filename': filename,
                                'message': message_data,
                                'timestamp': timestamp,
                                'status': status,
                                'processing_results': processing_results
                            })
                        except json.JSONDecodeError:
                            pass
        except Exception:
            pass
        socketio.emit('update_history', history_data)

    @app.route('/history/<filename>', methods=['GET'])
    def get_file_contents(filename):
        if not filename.endswith('.txt'):
            return jsonify({"error": "Invalid file type"}), 400

        history_dir = os.getenv('HISTDIR', './history')
        file_path = os.path.join(history_dir, filename)

        try:
            with open(file_path, 'r') as f:
                content = f.read()
            return content, 200
        except Exception:
            return jsonify({"error": "File not found or cannot be read"}), 404
        
    @app.route('/devices/<filename>', methods=['GET'])
    def get_device_details(filename):
        devices_dir = './devices'
        device_file_path = os.path.join(devices_dir, f"{filename}.json")
        try:
            with open(device_file_path, 'r') as f:
                device_info = json.load(f)
                print(device_info)
                return jsonify(device_info), 200
        except FileNotFoundError:
            return jsonify({'error': 'Device not found'}), 404
        except json.JSONDecodeError:
            return jsonify({'error': 'Error reading device data'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500


    @socketio.on('heartbeat')
    def update_heartbeat():
        return heartbeat()

    def heartbeat():
        global device_info  # Ensure we're working with the global variable
        heartbeat_interval = device_info.get("Heartbeat", 300)  # Default to 300 seconds
        # Update Last Updated timestamp
        device_info["Last Updated"] = time.strftime('%Y-%m-%d %H:%M:%S')
        save_device_info(heartbeat_interval)  # Save updated info

    # Schedule heartbeat every 5 minutes
    def heartbeat_scheduler():
        while True:
            time.sleep(10)  # Change to 300 for 5 minutes
            heartbeat()  # Call the heartbeat function

    # Start the heartbeat scheduler in a separate thread
    threading.Thread(target=heartbeat_scheduler, daemon=True).start()
