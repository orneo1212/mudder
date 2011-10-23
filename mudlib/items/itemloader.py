from item import Item
from mudlib.sys.loaders import get_items_files_list
import json
import mudlib
import os

class ItemLoader:
    def __init__(self):
        self.items={}

    def load_items(self):
        """Load items"""
        #If requested item is not loaded load it
        for itemfile in get_items_files_list():
            itempath=os.path.join(mudlib.rootpath, "data/items/%s" % itemfile)
            #try load data
            try:data=json.load(open(itempath))
            except Exception, e:
                print "EE Cannot load item from %s" % itempath
                print e
                continue
            #create room
            newitem=Item()
            newitem.uuid=data["uuid"]
            newitem.name=data["name"]
            newitem.desc=data["desc"]
            self.items[newitem.uuid]=newitem

    def get_item(self, uuid):
        """Return item by uuid"""
        try:
            return self.items[uuid]
        except:print "EE Item not exist but requested UUID=%s" % uuid
        return Item()