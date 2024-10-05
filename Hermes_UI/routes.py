import os
import json
from flask import render_template, jsonify

def init_routes(app, rules, socketio):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/rules', methods=['GET'])
    def get_rules():
        """Fetch the rules as a JSON response."""
        rules_data = {file: str(rule) for file, rule in rules.rules.items()}
        return jsonify(rules_data)

    @app.route('/history', methods=['GET'])
    def get_history():
        """Fetch the history files and their contents as a JSON response."""
        history_data = []
        history_dir = os.getenv('HISTDIR', './history')  # Ensure you get the history directory
        try:
            for filename in os.listdir(history_dir):
                if filename.endswith('.txt'):
                    file_path = os.path.join(history_dir, filename)
                    with open(file_path, 'r') as f:
                        content = f.read()
                        # Parse the JSON content
                        try:
                            message_data = json.loads(content.splitlines()[0])  # Assuming the first line is JSON
                            # Extract timestamp and status if available
                            timestamp = message_data.get('timestamp', 'N/A')
                            status = message_data.get('status', 'N/A')
                            processing_results = content.splitlines()[1:]  # The rest are processing results
                            history_data.append({
                                'filename': filename,  # Keep the filename for reference
                                'message': message_data,
                                'timestamp': timestamp,  # This can be kept if needed
                                'status': status,
                                'processing_results': processing_results
                            })
                        except json.JSONDecodeError:
                            print(f"Error decoding JSON from {filename}. Skipping...")
        except Exception as e:
            print(f"Error reading history directory: {e}")
    
        return jsonify(history_data)


    @app.route('/history/<filename>', methods=['GET'])
    def get_file_contents(filename):
        """Fetch the contents of a specific history file."""
        if not filename.endswith('.txt'):
            return jsonify({"error": "Invalid file type"}), 400

        history_dir = os.getenv('HISTDIR', './history')
        file_path = os.path.join(history_dir, filename)

        try:
            with open(file_path, 'r') as f:
                content = f.read()
            return content, 200
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
            return jsonify({"error": "File not found or cannot be read"}), 404
