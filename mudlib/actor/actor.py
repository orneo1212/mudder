from mudlib.items import globalitemloader
from mudlib.rooms import globalroomloader
from mudlib.sys.timer import Timer
import json
import mudlib
import os
import random

class Actor:
    def __init__(self, client):
        self.client=client # Telnet client object
        self.name=""
        self.password=""
        self.login_state=0 # 0: not logged 1: password 2:newcharacter 3: logged in 4: disconnect
        self.newingame=True
        self.inventory=[] # list of items
        self.sit=False # does player sit
        #RPG Stats
        self.level=1
        self.exp=[0, 100] # experiance poinst and to next level points
        self.hp=[30, 30] # Health points
        self.mp=[20, 20] # Mana points
        self.str=2 # Strength
        self.int=2 # Inteligence
        self.vit=2 # Vitality
        self.dex=2 # Dexterity
        #Survival Stats
        self.food=100.0 # Food if low actor is hungry
        self.water=100.0 # if low then actor is thirsty
        #locations
        self.location="r1" # uuid of room where actor is
        self.repawnlocation="r1" # uuid of room where actor respawn
        #State
        self.found_item=False # does actor found item in area #TODO: reset this on enter other location
        self.sit=False # actor sit True or False
        #Fight
        self.in_fight=False # does actor is in fight
        self.target=None # Fight target
        self.fightimer=Timer()
        #Rest
        self.resttimer=Timer()

    def get_item_by_name(self, partialname):
        """Return first item (object) from inventory matching given partialname"""
        for item in self.inventory:
            itemobj=globalitemloader.get_item(item)
            if partialname.lower() in itemobj.name.lower():
                return itemobj
        return None

    def moveto(self, newlocationid, silent=False):
        """Move player to new location"""
        room=self.get_room()
        if not silent:room.on_leave(self)
        self.location=str(newlocationid)
        #Call onenter on the next room
        room=self.get_room()
        if not silent:room.on_enter(self)

    def update(self):
        """Update player statistic"""
        #Rest if sitting
        if self.resttimer.timepassed(2000) and self.sit:
            self.hp[0]+=2
        #Health
        if self.hp[0]<0:self.hp[0]=0
        if self.hp[0]>self.hp[1]:self.hp[0]=self.hp[1]
        #mana
        if self.mp[0]<0:self.mp=0
        if self.mp[0]>self.mp[1]:self.mp[0]=self.mp[1]
        #water
        if self.water<0:self.water=0
        if self.water>100:self.water=100
        #food
        if self.food<0:self.food=0
        if self.food>100:self.food=100
        #Exp gain level
        if self.exp[0]>=self.exp[1]:
            self.levelup()
        # Continue fight
        if self.in_fight and self.target and self.fightimer.timepassed(1500):
            self.defend(self.target) # actor start defend against monster
            if self.target:self.target.defend(self)

    def defend(self, monster):
        """Defend against monster"""
        texts_atk=[
                   "^R\r %s zadaje ci %s obrazen.^~\n",
                   ]

        texts_dead=[
                    "^R\r i po tym uderzeniu padasz martwy na ziemie.^~\n",
                    "^R\r i to juz koniec twojej wizyty na tym swiecie.^~\n",
                    ]

        texts_dodge=[
                    "^R\r bylesz szybszy %s nie trafia cie.^~\n",
                    ]

        #calculate dodge
        dodge=float(monster.stats[2])/float(self.dex)
        dodge+=random.randint(-2, 2)
        dodge=dodge<0

        if not dodge:
            #Calculate monster damange
            dmg=float(monster.stats[0])/float(self.dex)*monster.stats[0]
            dmg=int(dmg)
            dmg+=random.randint(-5, 5)
            if dmg<0:dmg=0

            #decrase hp
            self.hp[0]-=dmg
            #show monster attack message
            text=random.choice(texts_atk)
            self.send(text % (monster.name, dmg))
            #check actor dead
            if self.hp[0]<=0:
                #actor die
                self.in_fight=False
                self.target=None
                text=random.choice(texts_dead)
                self.send(text)
                self.ondead()
        #Dodge
        else:
            text=random.choice(texts_dodge)
            self.send(text % monster.name)
        #send prompt to show hp
        self.send_prompt()

    def update_warrnings(self):
        if self.water<30:
            self.send("\r  Jestes spragniony\n")
        if self.food<30:
            self.send("\r  Jestes glodny\n")

    def onconnect(self):
        pass

    def ondisconnect(self):
        self.savedata()
        #Call onleave on the current room
        room=self.get_room()
        room.on_leave(self)

    def levelup(self):
        """increase player level and change exp to next level"""
        self.level+=1
        self.exp[1]=self.level**2*100
        self.hp[1] = int(self.hp[1]+self.hp[1]*0.1)
        self.mp[1] = int(self.mp[1]+self.mp[1]*0.1)
        self.hp[0]=self.hp[1]
        self.mp[0]=self.mp[1]
        self.send("^G\r  Teraz jestes o poziom bardziej doswiadczony.^~\n")

    def ondead(self):
        """On dead"""
        #Cancel fight
        self.in_fight=False
        self.target=None
        #
        self.send("^G\r/====================\\^~\n")
        self.send("^G\r  Bogowie Dali ci      ^~\n")
        self.send("^G\r  kolejna szanse       ^~\n")
        self.send("^G\r  nie zawiedz ich.     ^~\n")
        self.send("^G\r\\====================/^~\n")
        self.send("^G\r Zostales zeslany spowrotem do zywych. ^~\n")
        self.hp[0]=self.hp[1]
        #Lose experiance
        self.exp[0]-=int(self.exp[0]*0.10) # lose 10% of exp
        if self.exp[0]<0:self.exp[0]=0
        #change location
        room=self.get_room()
        room.on_leave(self)
        self.location=self.repawnlocation[:]
        #
        self.send_prompt()

    def loaddata(self):
        """Load actor data"""
        if not self.name:return
        actorfile=os.path.join(mudlib.rootpath, "data/players/"+self.name+".json")
        try:data=json.load(open(actorfile))
        except:
            print "EE Failed to load character file %s" % self.name
            return
        #load data here
        if data.has_key("location"):
            self.location=data["location"]
        if data.has_key("password"):
            self.password=data["password"]
        if data.has_key("hp"):
            self.hp=data["hp"]
        if data.has_key("level"):
            self.level=data["level"]
        if data.has_key("exp"):
            self.exp=data["exp"]
        if data.has_key("mp"):
            self.mp=data["mp"]
        if data.has_key("str"):
            self.str=data["str"]
        if data.has_key("int"):
            self.int=data["int"]
        if data.has_key("vit"):
            self.vit=data["vit"]
        if data.has_key("dex"):
            self.dex=data["dex"]
        if data.has_key("inventory"):
            self.inventory=data["inventory"]
        if data.has_key("food"):
            self.food=data["food"]
        if data.has_key("water"):
            self.water=data["water"]
        if data.has_key("repawnlocation"):
            self.repawnlocation=data["repawnlocation"]

    def savedata(self):
        """Save actor data"""
        if not self.name:return
        actorfile=os.path.join(mudlib.rootpath, "data/players/"+self.name+".json")

        data={}
        data["password"]=self.password
        data["level"]=self.level
        data["exp"]=self.exp
        data["hp"]=self.hp
        data["mp"]=self.hp
        data["str"]=self.str
        data["int"]=self.int
        data["vit"]=self.vit
        data["dex"]=self.dex
        data["location"]=self.location
        data["inventory"]=self.inventory
        data["food"]=self.food
        data["water"]=self.water
        data["repawnlocation"]=self.repawnlocation

        try:
            json.dump(data, open(actorfile, "w"), indent=2)
            print "II Actor %s saved. to %s" % (self.name, actorfile)
        except Exception, e:
            print "EE Failed to save character file %s" % self.name
            print e
            return

    def send_prompt(self):
        self.client.send_cc("HP:%s/%s # ^~" % (self.hp[0], self.hp[1]))

    def send(self, text):
        """Send text to client using send_cc"""
        self.client.send_cc(text)

    def get_room(self):
        """Return location where player is"""
        room=globalroomloader.get_room(self.location)
        return room