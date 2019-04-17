import os
import configparser

cpath = os.path.abspath(os.path.dirname(__file__))
cfg_path = os.path.join(cpath, "../config.cfg")

def load(section=None):
	config = configparser.ConfigParser()
	config.read(cfg_path)
	if section=None:
		return config['DEFAULT']
	else:
		return config[section]
