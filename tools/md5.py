#!/usr/bin/python
import hashlib

text=""

m=hashlib.md5()
m.update("SALT")
m.update(text)
print m.hexdigest()
