from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Load API key securely from environment variable
PI_API_KEY = os.getenv("PI_API_KEY", "tpvz4ebcvjqnzol1syplkbjkfypsz7lkwzm0hl1aldlrrufzrb0kdwz5w9aidbcc")

# Dummy user database (Replace with a real database)
users = {
    "user1": {"balance": 50, "private_key": "abc123"},
    "user2": {"balance": 30, "private_key": "xyz456"}
}

@app.route('/balance/<username>', methods=['GET'])
def get_balance(username):
    """Fetch balance of a user"""
    user = users.get(username)
    if user:
        return jsonify({"balance": user["balance"]})
    return jsonify({"error": "User not found"}), 404

@app.route('/send', methods=['POST'])
def send_pi():
    """Transfer Pi coins between users"""
    data = request.json
    sender = data.get("sender")
    receiver = data.get("receiver")
    amount = data.get("amount")

    if sender not in users or receiver not in users:
        return jsonify({"error": "User not found"}), 404

    if users[sender]["balance"] >= amount:
        users[sender]["balance"] -= amount
        users[receiver]["balance"] += amount
        return jsonify({"message": "Transaction successful!"})
    else:
        return jsonify({"error": "Insufficient balance"}), 400

@app.route('/pi_balance/<user_id>', methods=['GET'])
def get_pi_balance(user_id):
    """Fetch balance from Pi Network using API"""
    api_url = f"https://api.pi.network/user/{user_id}/balance"
    headers = {"Authorization": f"Bearer {PI_API_KEY}"}
    response = requests.get(api_url, headers=headers)
    return response.json()

# Required for Vercel serverless functions
def handler(event, context):
    return app(event, context)
