from mudlib.sys.loaders import get_rooms_files_list
from room import Room
import json
import mudlib
import os

class RoomLoader:
    def __init__(self):
        self.rooms={}

    def load_rooms(self):
        """Load rooms"""
        #If requested room is not loaded load it
        for roomfile in get_rooms_files_list():
            roompath=os.path.join(mudlib.rootpath, "data/rooms/%s" % roomfile)
            #try load data
            try:data=json.load(open(roompath))
            except Exception,e:
                print "EE Cannot load room from %s" % roompath
                print e
                continue
            #create room
            newroom=Room()
            newroom.uuid=data["uuid"]
            newroom.name=data["name"]
            newroom.desc=data["desc"]
            newroom.warps=data["warps"] #restore warps

            #for place in places:
            #    # [X,Y,roomUuid]
            #    newroom.places[place[1]][place[0]]=place[2]
            self.rooms[newroom.uuid]=newroom

    def get_room(self, uuid):
        """Return room by uuid"""
        try:
            return self.rooms[uuid]
        except:print "EE Room not exist but requested UUID=%s" % uuid
        return Room()