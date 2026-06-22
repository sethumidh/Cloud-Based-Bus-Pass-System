from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import random

app = Flask(__name__)
CORS(app)

# In-memory databases
USERS_DB = {}         # To store registered users {email: {password, name}}
APPLICATIONS_DB = {}  # To store submitted pass applications

# Locked routing pricing to prevent incorrect pricing
PASS_PRICING = {
    "Student Pass": 500.00,
    "Standard Pass": 1500.00,
    "Senior Pass": 800.00
}

# Traffic Metrics for dynamic cloud simulation
SERVER_METRICS = {
    "active_instances": 1,
    "current_load_percentage": 14.2,
    "server_status": "Stable (Optimal Load)"
}

def scale_cloud():
    current_load = round(random.uniform(20.0, 90.0), 2)
    SERVER_METRICS["current_load_percentage"] = current_load
    if current_load > 75.0:
        SERVER_METRICS["active_instances"] = random.randint(3, 5)
        SERVER_METRICS["server_status"] = "Scaling Active (High Traffic Dynamic Provisioning)"
    else:
        SERVER_METRICS["active_instances"] = 1
        SERVER_METRICS["server_status"] = "Stable (Optimal Load)"

@app.route('/register', methods=['POST'])
def register():
    scale_cloud()
    data = request.json
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if not name or not email or not password:
        return jsonify({"error": "All validation fields are required."}), 400
    
    if email in USERS_DB:
        return jsonify({"error": "User with this email already exists."}), 400

    USERS_DB[email] = {"name": name, "password": password}
    return jsonify({"success": True, "message": "Registration successful!"})

@app.route('/login', methods=['POST'])
def login():
    scale_cloud()
    data = request.json
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if email in USERS_DB and USERS_DB[email]['password'] == password:
        return jsonify({"success": True, "name": USERS_DB[email]['name']})
    
    return jsonify({"error": "Invalid email credentials or password."}), 401

@app.route('/submit_application', methods=['POST'])
def submit_application():
    scale_cloud()
    data = request.json
    
    pass_id = f"EBP-{random.randint(1000,9999)}EBP-{random.randint(1000,9999)}"
    
    app_record = {
        "pass_id": pass_id,
        "name": data.get('name'),
        "age": data.get('age'),
        "mobile": data.get('mobile'),
        "email": data.get('email'),
        "adhar": data.get('adhar'),
        "address": data.get('address'),
        "pass_type": data.get('pass_type'),
        "amount": PASS_PRICING.get(data.get('pass_type'), 500.00),
        "status": "Pending Payment"
    }
    
    APPLICATIONS_DB[pass_id] = app_record
    return jsonify({"success": True, "pass_id": pass_id, "amount": app_record["amount"]})

@app.route('/renew_pass', methods=['POST'])
def renew_pass():
    scale_cloud()
    data = request.json
    pass_id = data.get('pass_id', '').strip()

    if pass_id in APPLICATIONS_DB:
        APPLICATIONS_DB[pass_id]['status'] = "Renewed & Active"
        return jsonify({"success": True, "message": f"Pass {pass_id} successfully renewed!"})
    
    return jsonify({"error": "Pass ID not found in security database database."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)