
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

    def on_enter(self,actor):
        """callback on enter to this location"""
        self.players.append(actor)
        for player in self.players:
            if player!=actor:
                player.send("\rGracz ^Y%s^~ wszedl do lokacji\n" % actor.name)

    def on_leave(self,actor):
        """Callback on leave this location"""
        self.players.remove(actor)
        for player in self.players:
            if player!=actor:
                player.send("\rGracz ^Y%s^~ opuscil lokacje\n" % actor.name)