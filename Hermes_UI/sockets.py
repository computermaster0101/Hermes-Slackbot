import os
import json
import time
from rule_set import RuleSet
from message_processor import MessageProcessor
from message import Message
from dotenv import load_dotenv
from flask import render_template, jsonify

load_dotenv()
DEVICE = os.getenv('SYSNAME', 'missingName')
RULES_DIR = os.getenv('RULESDIR', './rules/win10')
HIST_DIR = os.getenv('HISTDIR', './history')
rules = RuleSet(RULES_DIR)
message_processor = MessageProcessor(rules)

def init_routes(app, socketio):
    @app.route('/')
    def index():
        return render_template('index.html')

    @socketio.on('send_message')
    def send_message(message):
        try:
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
