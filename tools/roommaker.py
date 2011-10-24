#!/usr/bin/python
import json
import hashlib
import random

#generate uuid
uuidmd5=hashlib.md5()
uuidmd5.update(str(random.random()))

data={}

data["uuid"]=uuidmd5.hexdigest()
data["name"]="Room Name"
data["desc"]="Room description"
data["exits"]={} # Dict of exits key=direction(nsew) value:roomUUID
data["searchitems"]=[] # ID of items to find in this area
data["monsters"]=[] # IDs of monsters to spawn

print json.dumps(data,indent=2)
