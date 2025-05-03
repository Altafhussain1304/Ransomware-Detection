from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

@app.route('/api/summary', methods=['GET'])
def get_summary():
    try:
        summary_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/logs/final_summary.json'))
        print("[DEBUG] Using path:", summary_path)
        with open(summary_path, 'r') as f:
            data = json.load(f)
        return jsonify(data), 200
    except Exception as e:
        print("[ERROR]", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
