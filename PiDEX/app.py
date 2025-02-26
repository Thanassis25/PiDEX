from flask import Flask, request, jsonify  # Import Flask modules for API handling
from flask_cors import CORS  # Enable cross-origin requests
import requests  # Library to make API requests

# Initialize Flask app
app = Flask(__name__)

# Enable CORS to allow frontend requests
CORS(app)

# Dummy database (Replace with real database like PostgreSQL or Firebase)
users = {
    "user1": {"balance": 50, "private_key": "abc123"},  # User 1 with 50 Pi
    "user2": {"balance": 30, "private_key": "xyz456"}   # User 2 with 30 Pi
}

# Your Pi Network API key (Replace this with a secure method of storing API keys)
PI_API_KEY = "tpvz4ebcvjqnzol1syplkbjkfypsz7lkwzm0hl1aldlrrufzrb0kdwz5w9aidbcc"

# API to check user balance
@app.route('/balance/<username>', methods=['GET'])
def get_balance(username):
    """ Fetch balance of a user """
    user = users.get(username)  # Get user data from dummy database
    if user:
        return jsonify({"balance": user["balance"]})  # Return balance as JSON response
    return jsonify({"error": "User not found"}), 404  # If user doesn't exist, return error

# API to send Pi coins from one user to another
@app.route('/send', methods=['POST'])
def send_pi():
    """ Transfer Pi coins between users """
    data = request.json  # Get data from frontend (JSON request)
    sender = data.get("sender")  # Sender username
    receiver = data.get("receiver")  # Receiver username
    amount = data.get("amount")  # Amount to transfer

    # Check if sender and receiver exist
    if sender not in users or receiver not in users:
        return jsonify({"error": "User not found"}), 404  # Return error if user doesn't exist

    # Check if sender has enough balance
    if users[sender]["balance"] >= amount:
        users[sender]["balance"] -= amount  # Deduct amount from sender
        users[receiver]["balance"] += amount  # Add amount to receiver
        return jsonify({"message": "Transaction successful!"})  # Return success message
    else:
        return jsonify({"error": "Insufficient balance"}), 400  # Return error if not enough funds

# API to get balance from Pi Network
@app.route('/pi_balance/<user_id>', methods=['GET'])
def get_pi_balance(user_id):
    """ Fetch balance from Pi Network using API """
    api_url = f"https://api.pi.network/user/{user_id}/balance"  # API endpoint
    headers = {"Authorization": f"Bearer {PI_API_KEY}"}  # Add API Key in headers

    response = requests.get(api_url, headers=headers)  # Make request to Pi API
    return response.json()  # Return API response

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

