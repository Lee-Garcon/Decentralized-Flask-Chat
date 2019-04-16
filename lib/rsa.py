import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
import os
import base64
import hashlib

class RSA_Local:
	def __init__(self, name):
		self.name = name
		self.load()

	def generate(self):

		key = RSA.generate(2048)
		pubkey = key.publickey().exportKey("PEM").decode("utf-8")
		privkey = key.exportKey("PEM").decode("utf-8")
	
		f = open(self.public_path, 'w')
		f.write(pubkey)
		f.close()
	
		f = open(self.private_path, 'w')
		f.write(privkey)
		f.close()
	
		return RSA.importKey(pubkey), RSA.importKey(privkey)

	def load(self):

		cpath = os.path.abspath(os.path.dirname(__file__))

		self.list_path = os.path.join(cpath, "../keys/keys.lst")
		self.public_path = os.path.join(cpath, "../keys/public_%s.pem" % self.name)
		self.private_path = os.path.join(cpath, "../keys/private_%s.pem" % self.name)

		try:
			f = open(self.public_path, 'r')
			self.pubkey = RSA.importKey(f.read())
			f.close()

			f = open(self.private_path, 'r')
			self.privkey = RSA.importKey(f.read())
			f.close()
		except:
			self.pubkey, self.privkey = self.generate()

	def encrypt(self, data):
		cipher = PKCS1_OAEP.new(self.pubkey)
		return base64.b64encode(cipher.encrypt(data.encode("utf-8"))).decode("utf-8")

	def decrypt(self, data):
		cipher = PKCS1_OAEP.new(self.privkey)
		return cipher.decrypt(base64.b64decode(data.encode("utf-8"))).decode("utf-8")

	def decrypt_bytes(self, data):
		cipher = PKCS1_OAEP.new(self.privkey)
		return cipher.decrypt(base64.b64decode(data.encode("utf-8")))

	def key_transport(self):
		key = self.pubkey
		return base64.b64encode(key.exportKey("PEM")).decode("utf-8")

	def validate_handshake_reply(self, reply):
		bytestring = self.decrypt_bytes(reply)
		message = bytestring[:12].decode("utf-8")
		if message == "payloadreply":
			return True
		else:
			return False


class RSA_Guest:
	def __init__(self, name, pubkey):
		self.name = name
		self.load(pubkey)

	def load(self, provided_pubkey):
		cpath = os.path.abspath(os.path.dirname(__file__))
		self.keypath = os.path.join(cpath, "../keys/%s.pem" % self.name)
		
		try:
			f = open(self.keypath, 'r')
			self.pubkey = RSA.importKey(f.read())
			f.close()
		except:
			self.pubkey = RSA.importKey(self.key_decode(provided_pubkey))

	def encrypt(self, data):
		cipher = PKCS1_OAEP.new(self.pubkey)
		return base64.b64encode(cipher.encrypt(data.encode("utf-8"))).decode("utf-8")

	def encrypt_bytes(self, data):
		cipher = PKCS1_OAEP.new(self.pubkey)
		return base64.b64encode(cipher.encrypt(data)).decode("utf-8")

	def key_decode(self, data):
		return base64.b64decode(data.encode("utf-8")).decode("utf-8")

	def handshake_reply(self):
		payload = b"payloadreply" + generate_salt()
		return self.encrypt_bytes(payload)

def load_RSA_profiles():
	cpath = os.path.abspath(os.path.dirname(__file__))
	lister_path = os.path.join(cpath, "../keys/keys.lst")

	f = open(lister_path)
	profiles_list = [x.strip() for x in f.readlines()]
	f.close()

	profiles = {}
	locals = {}

	for path in profiles_list:
		name = path.split('/')[-1].split('.')[0]
		is_local_user = name.startswith("public_") or name.startswith("private_")
		if is_local_user and len("_".join(name.split('_')[1:])) > 3:
			#Is local user
			name = "_".join(name.split('_')[1:])
			if not profiles.get(name):
				profiles[name] = RSA_Local(name)

		else:
			profiles[name] = RSA_Guest(name, None)

	return profiles

def generate_salt(seed=Random.get_random_bytes(16)):

	s = seed

	for i in range(16):
		s = hashlib.sha256(s).digest()

	return s



if __name__ == "__main__":
	message = "this is an extra-long message. I wonder how long it would be. Test test Test test Test!"
	self_rsa = RSA_Local("dylwall")
	guest_rsa = RSA_Guest("dylwall", self_rsa.key_transport())

	rsa_ciphertext = guest_rsa.encrypt(message)
	print(rsa_ciphertext)

	rsa_original = self_rsa.decrypt(rsa_ciphertext)
	print(rsa_original)

	print("== == == == == == ==")

	handshake_reply = guest_rsa.handshake_reply()
	print(handshake_reply)

	handshake_reply_validation = self_rsa.validate_handshake_reply(handshake_reply)
	if handshake_reply_validation:
		print("verified!")
	else:
		print(self_rsa.decrypt(handshake_reply))
