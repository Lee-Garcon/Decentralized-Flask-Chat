import time


class Message:
	def __init__(self, content, time, id, rsa_local):
		self.id = id
		self.content = content
		self.time = time
		self.creation_time = time.time()
		self.rsa_local = rsa_local
		self.decoded = self.decode(rsa_local)

	def decode(self, rsa_local):
		return rsa_local.decrypt(self.content)

	def serialize(self):
		return {
			'id': self.id,
			'content': self.decoded,
			'creation': self.time,
			'recieved': self.creation_time
			}
