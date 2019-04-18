from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS, cross_origin
import hashlib, time
import lib.rsa as rsa
import lib.read_cfg as rcfg
import lib.img_b64 as img64
import lib.message_handler as msg
import os

#=== === === Paths === === ===
cpath = os.path.abspath(os.path.dirname(__file__))
rootpath = os.path.join(cpath, "..")

#=== === === Funcs === === ===

def is_localhost(url):
	stripped = url.replace('https://', '')
	stripped = stripped.replace('http://', '')

	if stripped.startswith('localhost'):
		stripped = stripped.replace('localhost', '')
		if stripped.startswith(':'):
			return True
	return False

def obj_dict(object):
	if type(object) is list:
		return [x.serialize() for x in object]
	elif type(object) is dict:
		return {k:v.serialize() for (k, v) in object.items()}
	else:
		return object.serialize()

#=== === === Setup === === ===
config = rcfg.load()
NAME = config["name"]

MESSAGES = []
IDS = {}

RSA_PROFILES = rsa.load_RSA_profiles()

if NAME not in RSA_PROFILES.keys():
	RSA_PROFILES[NAME] = rsa.RSA_Local(NAME)

MYKEY = RSA_PROFILES[NAME].key_transport()


template_dir = os.path.join(rootpath, "templates")
app = Flask(__name__, template_folder=template_dir)
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/sys/inbound', methods=['POST', 'OPTIONS'])
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
		try:
			name = request.json.get('name')
			message = request.json.get('message')
			sent_time = int(request.json.get('time'))
			if name not in MESSAGES.keys():
				MESSAGES[name] = []
			if name not in IDS.keys():
				IDS[name] = hashlib.md5(name.encode('utf-8')).hexdigest()
			MESSAGES.append(msg.Message(message, sent_time, IDS[name]))
			return 200
		except:
			return 400


@app.route('/handshake', methods=['POST', 'OPTIONS'])
@cross_origin()
def handshake():
	if request.form.get("action") == "initiate-handshake":
		# handshake initiation
		addr = request.form.get("recipient")
		data = {"type": "handshake-request",
			"key": MYKEY,
			"name": NAME}

		r = requests.post(url=addr+'/sys/inbound', data=data)
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
@cross_origin()
def client():
	if request.method == 'GET':
		return render_template('client.html', name=NAME)
	elif request.method == 'POST':
		pass

@route('/sys/send_message', methods=['POST', 'OPTIONS'])
@cross_origin()
def send():
	if request.method == 'POST':
		try:
			addr = request.json.get('recipient')
			message = request.json.get('message')
			data = {"type": "message",
				"name": NAME,
				"message": message,
				"time": str(time.time())}
			r = requests.post(addr+'/sys/inbound', data=data)
			return jsonify({'code': r.code}), 200
		except:
			return 400

@app.route('/sys/get_messages', methods=['POST', 'OPTIONS'])
@cross_origin()
def getmessages():
	if request.method == 'POST':
		origin = request.base_url
		if is_localhost(origin):
			data = obj_dict(MESSAGES)
			return jsonify(data), 200
		return 400

@app.route('/sys', methods=['POST', 'OPTIONS'])
@cross_origin()
def sys():
	if request.method == 'POST':
		pass
