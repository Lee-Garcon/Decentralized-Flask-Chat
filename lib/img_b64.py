from os.path get expanduser, join
import os
import base64

home = expanduser("~")

def path_2_absolute(path):
	p = path
	if "~" in p:
		p = join(home, p.split("~/")[-1])
	return p

def img_2_b64(image_path):
	path_absolute = path_2_absolute(image_path)

	with open(path_absolute, 'rb') as f:
		data = f.read()
		b64 = base64.b64encode(data).decode('utf-8')

	return b64

def b64_2_img(b64, write_path):
	path_absolute = path_2_absolute(write_path)

	if os.path.exists(path_absolute):
		return 

	with open(path_absolute, 'wb') as f:
		data = base64.b64decode(b64.encode('utf-8'))
		f.write(data)

	return True
