from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS, cross_origin
import hashlib, time
import lib.rsa as rsa
import lib.read_cfg as rcfg
import lib.img_b64.py as img64
import os

#=== === === Paths === === ===
cpath = os.path.abspath(os.path.dirname(__file__))
rootpath = os.path.join(cpath, "..")

#=== === === Setup === === ===
config = rcfg.load()
NAME = config["name"]

MESSAGES = {}
RSA_PROFILES = rsa.load_RSA_profiles()

if NAME not in RSA_PROFILES.keys():
	RSA_PROFILES[NAME] = rsa.RSA_Local(NAME)

MYKEY = RSA_PROFILES[NAME].key_transport()


template_dir = os.path.join(rootpath, "templates")
app = Flask(__name__, template_folder=template_dir)
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/inbound', methods=['POST', 'OPTIONS'])
def result():
	req_type = request.json.get("type")
	if req_type == "handshake-request":
		name = request.json.get("name")
		RSA_key = request.json.get("key")
		if (not name or not key):
			return 400
		if name not in RSA_PROFILES.keys():
			RSA_PROFILES[name] = rsa.RSA_Guest(RSA_key)

		handshake_reply = RSA_PROFILES[name].handshake_reply()

		timeout = time.time() + 3600
		data = {"type": "handshake-reply",
			"timeout": str(timeout),
			"handshake-reply": handshake_reply,
			"key": MYKEY,
			"name": NAME}

		return jsonify(data), 200

	elif req_type == "handshake-response":
		success = request.json.get("success")
		handshake_reply = request.json.get("handshake_reply")
		name = request.json.get("name")
		if RSA_PROFILES[name].validate_handshake_reply(handshake_reply) and success == 1:
			data = {"type": "handshake-success",
				"success": 1}
			return jsonify(data), 200
		else:
			return 400
		
	elif req_type == "message":
		


@app.route('/handshake', methods=['POST', 'OPTIONS'])
@cross_origin()
def handshake():
	if request.form.get("action") == "initiate-handshake":
		# handshake initiation
		addr = request.form.get("recipient")
		data = {"type": "handshake-request",
			"key": MYKEY,
			"name": NAME}

		r = requests.post(url=addr+'/inbound', data=data)
		response = r.json()

		rcp_name = response['name']
		timeout = int(response['timeout'])
		handshake_reply = response['handshake-reply']
		rcp_key = response['key']
		if RSA_PROFILES[NAME].validate_handshake_reply(handshake_reply):
			RSA_PROFILES[rcp_name] = rsa.RSA_Guest(rcp_key)
			data = {"type": "handshake-response",
				"name": NAME,
				"success": 1,
				"handshake-reply": RSA_PROFILES[rcp_name].handshake_reply()}

			r = requests.post(addr, data=data)
			return r.code
		else:
			return 400

@app.route('/client', methods=['GET', 'POST', 'OPTIONS'])
def client():
	if request.method == 'GET':
		return render_template('client.html', name=NAME)
	elif request.method == 'POST':
		pass
	
@route('/sendmessage', methods=['POST', 'OPTIONS'])
def send():
	if request.method == 'POST':
		addr = request.json.get('recipient')
		message = request.json.get('message')
		data = {"type": "message",
			"name": NAME,
			"message": message}
		r = requests.post(addr+'/inbound', data=data)
		return r.code
	
@app.route('/sys', methods=['POST', 'OPTIONS'])
def sys():
	if request.method == 'POST':
		pass
		
@app.route('/sys/update', methods['POST', 'OPTIONS'])
def update():
	if request.method == 'POST':
		pass
