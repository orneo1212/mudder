from monster import Monster
from mudlib.sys.loaders import get_monsters_files_list
import json
import mudlib
import os

class MonsterLoader:
    def __init__(self):
        self.monsters={}

    def load_monsters(self):
        """Load monsters"""
        #If requested monsters is not loaded load it
        for monstersfile in get_monsters_files_list():
            monsterspath=os.path.join(mudlib.rootpath, "data/monsters/%s" % monstersfile)
            #try load data
            try:data=json.load(open(monsterspath))
            except Exception, e:
                print "EE Cannot load monsters from %s" % monsterspath
                print e
                continue
            #create monster
            newmonster=Monster(data["uuid"])
            #newmonster.uuid=data["uuid"]
            newmonster.name=data["name"]
            newmonster.desc=data["desc"]
            self.monsters[newmonster.uuid]=newmonster

    def get_monster(self, uuid):
        """Return monster by uuid"""
        try:
            return self.monsters[uuid]
        except:print "EE Monster not exist but requested UUID=%s" % uuid
        return Monster(uuid)