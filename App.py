from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

users = {}
events = {}

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    users[email] = {
        "name": data.get('name', email.split('@')[0]),
        "gender": data.get('gender', 'male'),
        "paid": True
    }
    return jsonify({"message": "✅ $20 Payment Successful! Welcome to Zoom Speed Dating", "user": users[email]})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    if email in users:
        return jsonify({"message": "Login successful", "user": users[email]})
    return jsonify({"error": "User not found. Register first."}), 401

@app.route('/api/events', methods=['POST'])
def create_event():
    event_id = str(len(events) + 1)
    events[event_id] = {"participants": [], "rounds": 10}
    return jsonify({"event_id": event_id, "message": "Event created successfully"})

@app.route('/api/join/<event_id>', methods=['POST'])
def join_event(event_id):
    return jsonify({"message": "✅ Joined event! Zoom links will be sent before start."})

@app.route('/api/zoom-link', methods=['GET'])
def get_zoom_link():
    return jsonify({"zoom_link": "https://zoom.us/j/1234567890?pwd=DemoPassword"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
