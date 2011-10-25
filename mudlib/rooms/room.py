from mudlib.items import globalitemloader

class Room:
    def __init__(self):
        self.uuid=""
        self.name=""
        self.desc=""
        #
        self.exits={} # Exits
        self.items=[] # Items on the ground
        self.searchitems=[] # items to find with search [uuid,chance]
        self.players=[] # list of players in this room
        self.monsters=[] # List of monsters in this area (objects)
        self.possible_monsters=[] # monsters possible to spawn

    def get_item_by_name(self, partialname):
        """Return first item(obj) from ground matching partial name"""
        for item in self.items:
            itemobj=globalitemloader.get_item(item)
            if partialname.lower() in itemobj.name.lower():
                return itemobj
        return None

    def get_monster_by_name(self, partialname):
        """Return first monster(obj) matching partial name"""
        for monster in self.monsters:
            #show info about matching item/place
            if partialname.lower() in monster.name.lower():
                return monster
        return None

    def get_actor_by_name(self, partialname):
        """Return first actor(obj) matching partial name"""
        for actor in self.players:
            if partialname.lower() in actor.name.lower():
                return actor
        return None

    def broadcast(self, text, sender=None):
        """Broadcast message for all actors in room"""
        for actor in self.players:
            if actor==sender:continue
            actor.send(text)

    def on_enter(self, actor):
        """callback on enter to this location"""
        self.players.append(actor)
        for player in self.players:
            if player!=actor:
                player.send("\rGracz ^Y%s^~ wszedl do lokacji\n" % actor.name)

    def on_leave(self, actor):
        """Callback on leave this location"""
        if actor in self.players:self.players.remove(actor)
        actor.in_fight=False
        for player in self.players:
            if player!=actor:
                player.send("\rGracz ^Y%s^~ opuscil lokacje\n" % actor.name)