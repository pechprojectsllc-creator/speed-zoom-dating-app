from flask import Flask, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
import stripe
import os

app = Flask(__name__)
CORS(app)

# === SET YOUR STRIPE KEY HERE (from Stripe dashboard) ===
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_your_test_key_here')   # Change to live key later

users = {}
events = {}

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'Zoom Speed Dating Membership'},
                    'unit_amount': 2000,   # $20.00
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://your-deployed-url.onrender.com/success',
            cancel_url='https://your-deployed-url.onrender.com/',
            customer_email=email,
        )
        users[email] = {"email": email, "paid": False}
        return jsonify({"url": session.url})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    if email in users:
        return jsonify({"message": "Login successful", "user": users[email]})
    return jsonify({"error": "User not found"}), 401

@app.route('/api/events', methods=['POST'])
def create_event():
    event_id = str(len(events) + 1)
    events[event_id] = {"participants": [], "rounds": 10}
    return jsonify({"event_id": event_id, "message": "Event created"})

@app.route('/api/join/<event_id>', methods=['POST'])
def join_event(event_id):
    return jsonify({"message": "Joined! Zoom links coming soon."})

@app.route('/success')
def success():
    return "<h1>Payment Successful! Welcome to Zoom Speed Dating 🎉</h1><p><a href='/'>Go to App</a></p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
