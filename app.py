#!/usr/bin/env python3
"""
Flask app — DevSecOps M3 Lab
All SAST findings resolved.
"""
 
import os
import logging
from flask import Flask, request, jsonify
 
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
logger = logging.getLogger(__name__)
 
app = Flask(__name__)
 
 
@app.route('/health')
def health():
    return jsonify({
        "status": "ok",
        "version": "1.0",
        "uptime": 999
    })
 
 
@app.route('/version')
def version():
    return jsonify({"version": "1.0.0"})
 
 
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
 
    if not data:
        return jsonify({"error": "Invalid request body"}), 400
 
    username = data.get('username', '').strip()
    password = data.get('password', '')
 
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
 
    # Log attempt — never log the password
    logger.info(f"Login attempt: username={username} ip={request.remote_addr}")
 
    # Placeholder — real auth would check database with parameterised query
    return jsonify({"message": "login endpoint"})
 
 
@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "logged out"})
 
 
@app.route('/profile')
def profile():
    return jsonify({"user": "unknown"})
 
 
@app.route('/crash')
def crash():
    raise Exception("Intentional crash for demo")
 
 
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404
 
 
@app.errorhandler(500)
def server_error(e):
    # Log full error server-side
    logger.error(f"Internal error: {e}", exc_info=True)
    # Return generic message to client
    return jsonify({"error": "Internal server error"}), 500
 
 
if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', debug=debug_mode)