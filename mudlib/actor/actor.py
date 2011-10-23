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
        self.pos=[0,0]
        #RPG Stats
        self.hp=[100, 100] # Health points
        self.mp=[100, 100] # Mana points
        self.str=10 # Strength
        self.int=10 # Inteligence
        self.vit=10 # Vitality
        self.dex=10 # Dexterity
        #
        self.location="ae97b6d290c722114f5631e5aab51c4a" # uuid of room where actor is

    def onconnect(self):
        pass

    def ondisconnect(self):
        self.savedata()

    def loaddata(self):
        """Load actor data"""
        if not self.name:return
        actorfile=os.path.join(mudlib.rootpath, "data/players/"+self.name+".json")
        try:data=json.load(open(actorfile))
        except:
            print "EE Failed to load character file %s" % self.name
            return
        #load data here
        self.password=data["password"]
        self.hp=data["hp"]
        self.mp=data["mp"]
        self.str=data["str"]
        self.int=data["int"]
        self.vit=data["vit"]
        self.dex=data["dex"]

    def savedata(self):
        """Save actor data"""
        if not self.name:return
        actorfile=os.path.join(mudlib.rootpath, "data/players/"+self.name+".json")

        data={}
        data["password"]=self.password
        data["hp"]=self.hp
        data["mp"]=self.hp
        data["str"]=self.str
        data["int"]=self.int
        data["vit"]=self.vit
        data["dex"]=self.dex

        try:
            json.dump(data, open(actorfile, "w"), indent=2)
            print "II Actor %s saved. to %s" % (self.name, actorfile)
        except Exception, e:
            print "EE Failed to save character file %s" % self.name
            print e
            return

    def send_prompt(self):
        self.client.send_cc("# ")