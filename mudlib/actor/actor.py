import json
import mudlib
import os

class Actor:
    def __init__(self, client):
        self.client=client # Telnet client object
        self.name=""
        self.password=""
        self.login_state=0 # 0: not logged 1: password 2:newcharacter 3: logged in 4: disconnect
        self.newingame=True
        #
        self.location="" # uuid of room where actor is

    def loaddata(self):
        """Load actor data"""
        if not self.name:return
        actorfile=os.path.join(mudlib.rootpath,"data/players/"+self.name+".json")
        try:data=json.load(open(actorfile))
        except:
            print "EE Failed to load character file %s" % self.name
            return
        #load data here
        if data.has_key("password"):
            self.password=data["password"]

    def savedata(self):
        """Save actor data"""
        if not self.name:return
        actorfile=os.path.join(mudlib.rootpath,"data/players/"+self.name+".json")

        data={}
        data["password"]=self.password

        try:json.dump(data,open(actorfile))
        except:
            print "EE Failed to save character file %s" % self.name
            return