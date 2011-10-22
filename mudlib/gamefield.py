from mudlib.rooms.room import Room

class GameField:
    def __init__(self, actors):
        self.actors=actors

    def update(self):
        """Update the gamefield"""

        #update actors
        for actor in self.actors.values():

            #broadcast about new players
            if actor.newingame and actor.login_state==3:
                self.broadcast("%s joined the game." % actor.name)
                actor.newingame=False

    def recv(self, actor, cmd):
        """Received command from actor"""

        if cmd=="quit":actor.client.deactivate()
        if cmd=="look":self.look(actor)
        if cmd=="help":self.showhelp(actor)

    def broadcast(self, message):
        """broadcast message to all actors"""
        for actor in self.actors.values():
            actor.client.send_cc(message)

    def showhelp(self,actor):
        """Show help"""
        actor.client.send_cc("^gHELP:^~ Commands: help quit look\n")

    def look(self,actor):
        pass