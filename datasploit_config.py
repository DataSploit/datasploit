#!/usr/bin/env python

import os, subprocess, tempfile

def edit():
	config_path = os.path.dirname(__file__)
	config_file = "%s/config.py" % config_path
	if not os.path.exists(config_file):
		print("[+] Looks like a new setup, setting up the config file.")
		os.rename("%s/config_sample.py" % config_path, config_file)
	fh = open(config_file)
	config = fh.read()
	fh.close()
	f, fname = tempfile.mkstemp()
	fh = open(fname, "w")
	fh.write(config)
	fh.close()

	cmd = os.environ.get('EDITOR', 'vi') + ' ' + fname
	subprocess.call(cmd, shell = True)

	with open(fname, "r") as f:
		config = f.read().strip()
		fh = open(config_file, "w")
		fh.write(config)
		fh.close()

	os.unlink(fname)

if __name__ == "__main__":
	edit()
