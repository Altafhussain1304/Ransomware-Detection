from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Endpoint 1: Final Summary (Old)
@app.route('/api/summary', methods=['GET'])
def get_summary():
    try:
        summary_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/logs/final_summary.json'))
        print("[DEBUG] Using path:", summary_path)
        with open(summary_path, 'r') as f:
            data = json.load(f)
        return jsonify(data), 200
    except Exception as e:
        print("[ERROR] /api/summary:", str(e))
        return jsonify({'error': str(e)}), 500

# Endpoint 2: Monitor Summary (New)
@app.route('/api/monitor-summary', methods=['GET'])
def get_monitor_summary():
    try:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/logs/monitor/summary_for_ui.json'))
        print("[DEBUG] Using path:", path)
        with open(path, 'r') as f:
            data = json.load(f)
        return jsonify(data), 200
    except Exception as e:
        print("[ERROR] /api/monitor-summary:", str(e))
        return jsonify({'error': str(e)}), 500

# Endpoint 3: Simulated Summary (New)
@app.route('/api/simulated-summary', methods=['GET'])
def get_simulated_summary():
    try:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/logs/simulated/summary_for_ui.json'))
        print("[DEBUG] Using path:", path)
        with open(path, 'r') as f:
            data = json.load(f)
        return jsonify(data), 200
    except Exception as e:
        print("[ERROR] /api/simulated-summary:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
