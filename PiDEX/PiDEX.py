from flask import Flask, jsonify, request  # Import Flask for web framework and request handling
import requests  # Import requests to interact with Pi Network API

app = Flask(__name__)  # Initialize Flask app

# Pi Network API Key (Replace with your actual key)
API_KEY = "tpvz4ebcvjqnzol1syplkbjkfypsz7lkwzm0hl1aldlrrufzrb0kdwz5w9aidbcc"

# Liquidity pool (stores Pi and USDT balances)
liquidity_pool = {
    "pi": 1000,  # Initial Pi Liquidity
    "usdt": 1000  # Initial USDT Liquidity
}

# Developer commission fee (0.1%)
DEVELOPER_FEE_PERCENTAGE = 0.001

# Constant Product Market Maker (x * y = k) function to determine swap output
def get_swap_output(input_amount, input_reserve, output_reserve):
    input_amount_with_fee = input_amount * 997  # 0.3% total fee applied to swap
    developer_fee = input_amount * DEVELOPER_FEE_PERCENTAGE  # 0.1% developer commission
    numerator = input_amount_with_fee * output_reserve  # Calculate numerator for swap equation
    denominator = (input_reserve * 1000) + input_amount_with_fee  # Calculate denominator for swap equation
    return numerator / denominator, developer_fee  # Return the final swap output amount and dev fee

@app.route('/')  # Root route
def home():
    return "<h1>Pi DEX is Live!</h1><p>Use API endpoints to trade.</p>"  # Display a simple home page

# Authentication Endpoint
@app.route('/login', methods=['POST'])  # Define login route
def login():
    data = request.get_json()  # Get JSON data from request
    user_token = data.get("token")  # Extract user token
    if not user_token:  # Check if token is missing
        return jsonify({"error": "Missing authentication token"}), 400  # Return error response
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}  # Set headers
    response = requests.post("https://api.minepi.com/v2/auth", headers=headers, json={"token": user_token})  # Send authentication request
    return jsonify(response.json()), response.status_code  # Return response from Pi Network

# Swap Pi for USDT with developer commission
@app.route('/swap/pi-to-usdt', methods=['POST'])  # Define Pi to USDT swap route
def swap_pi_to_usdt():
    data = request.get_json()  # Get JSON data from request
    pi_amount = data.get("pi_amount", 0)  # Extract Pi amount from request
    if pi_amount <= 0:  # Validate input amount
        return jsonify({"error": "Invalid swap amount"}), 400  # Return error response
    usdt_received, developer_fee = get_swap_output(pi_amount, liquidity_pool["pi"], liquidity_pool["usdt"])  # Calculate USDT output
    liquidity_pool["pi"] += pi_amount - developer_fee  # Update Pi reserve in liquidity pool minus dev fee
    liquidity_pool["usdt"] -= usdt_received  # Update USDT reserve in liquidity pool
    return jsonify({"pi_spent": pi_amount, "usdt_received": usdt_received, "developer_fee": developer_fee})  # Return swap details

# Swap USDT for Pi with developer commission
@app.route('/swap/usdt-to-pi', methods=['POST'])  # Define USDT to Pi swap route
def swap_usdt_to_pi():
    data = request.get_json()  # Get JSON data from request
    usdt_amount = data.get("usdt_amount", 0)  # Extract USDT amount from request
    if usdt_amount <= 0:  # Validate input amount
        return jsonify({"error": "Invalid swap amount"}), 400  # Return error response
    pi_received, developer_fee = get_swap_output(usdt_amount, liquidity_pool["usdt"], liquidity_pool["pi"])  # Calculate Pi output
    liquidity_pool["usdt"] += usdt_amount - developer_fee  # Update USDT reserve in liquidity pool minus dev fee
    liquidity_pool["pi"] -= pi_received  # Update Pi reserve in liquidity pool
    return jsonify({"usdt_spent": usdt_amount, "pi_received": pi_received, "developer_fee": developer_fee})  # Return swap details

# Check Liquidity Pool Balances
@app.route('/liquidity', methods=['GET'])  # Define liquidity check route
def get_liquidity():
    return jsonify(liquidity_pool)  # Return current liquidity pool balances

# Add Liquidity
@app.route('/liquidity/add', methods=['POST'])  # Define add liquidity route
def add_liquidity():
    data = request.get_json()  # Get JSON data from request
    pi_amount = data.get("pi_amount", 0)  # Extract Pi amount from request
    usdt_amount = data.get("usdt_amount", 0)  # Extract USDT amount from request
    if pi_amount <= 0 or usdt_amount <= 0:  # Validate input amounts
        return jsonify({"error": "Invalid liquidity amount"}), 400  # Return error response
    liquidity_pool["pi"] += pi_amount  # Update Pi reserve in liquidity pool
    liquidity_pool["usdt"] += usdt_amount  # Update USDT reserve in liquidity pool
    return jsonify({"message": "Liquidity added", "new_pool": liquidity_pool})  # Return confirmation message

if __name__ == '__main__':  # Run the Flask app
    app.run(debug=True)  # Start Flask application in debug mode
