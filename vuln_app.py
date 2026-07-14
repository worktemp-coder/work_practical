#!/usr/bin/env python3
"""
INTENTIONALLY VULNERABLE FLASK APP
For SAST training purposes only.
Do NOT deploy this code.
"""

import sys

if __name__ != "__main__":
    print("ERROR: vuln_app is intentionally vulnerable and must NOT be imported.", file=sys.stderr)
    print("It is for isolated SAST/dependency scanning training only.", file=sys.stderr)
    sys.exit(1)

import os
import sqlite3
import subprocess
import hashlib
import pickle
import random
import yaml
from flask import Flask, request, jsonify

app = Flask(__name__)

# ── B105: Hardcoded password ──────────────────────
SECRET_KEY = "hardcoded-secret-key-123"
ADMIN_PASSWORD = "admin123"
API_KEY = "sk-prod-abc123xyz"

# ── B201: Flask debug mode ────────────────────────
# Will be flagged by B201

# ── A03: SQL Injection ────────────────────────────
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    conn = sqlite3.connect('users.db')
    # B608: SQL injection via string formatting
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = conn.execute(query).fetchone()
    conn.close()
    
    return jsonify({"logged_in": bool(result)})


# ── A02: Weak Cryptography ────────────────────────
@app.route('/hash-password', methods=['POST'])
def hash_password():
    password = request.json.get('password')
    
    # B303: Use of MD5 (not for passwords!)
    hashed = hashlib.md5(password.encode()).hexdigest()
    return jsonify({"hash": hashed})


# ── OS Command Injection ──────────────────────────
@app.route('/ping', methods=['POST'])
def ping_host():
    host = request.json.get('host')
    
    # B602: subprocess with shell=True is dangerous
    result = subprocess.run(
        f"ping -c 1 {host}",
        shell=True,
        capture_output=True,
        text=True
    )
    return jsonify({"output": result.stdout})


# ── Insecure Deserialization ──────────────────────
@app.route('/load-data', methods=['POST'])
def load_data():
    data = request.json.get('data')
    
    # B301: pickle.loads is dangerous with untrusted data
    obj = pickle.loads(bytes.fromhex(data))
    return jsonify({"loaded": str(obj)})


# ── Weak Random Number ────────────────────────────
@app.route('/generate-token', methods=['GET'])
def generate_token():
    # B311: random is not cryptographically secure
    token = str(random.randint(100000, 999999))
    return jsonify({"token": token})


# ── YAML Deserialization ──────────────────────────
@app.route('/parse-yaml', methods=['POST'])
def parse_yaml():
    data = request.json.get('yaml_data')
    
    # B506: yaml.load without Loader is dangerous
    parsed = yaml.load(data)
    return jsonify({"parsed": parsed})


# ── Hardcoded bind to all interfaces ─────────────
@app.route('/health')
def health():
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    # B201: debug=True exposes debugger
    app.run(host='0.0.0.0', debug=True)