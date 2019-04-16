from flask import Flask, request, jsonify
import hashlib, time
import lib.rsa as rsa
import lib.read_cfg as rcfg
import os

#=== === === Setup === === ===
config = rcfg.load()
NAME = config["name"]

RSA_PROFILES = rsa.load_RSA_profiles()

if NAME not in RSA_PROFILES.keys():
	RSA_PROFILES[NAME] = rsa.RSA_Local(NAME)





app = Flask(__name__)

@app.route('/inbound', methods=['POST'])
def result():
	req_type = request.json.get("type")
	if req_type == "handshake":
	
