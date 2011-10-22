from mudlib.rooms import globalroomloader

class GameField:
    def __init__(self, actors):
        self.actors=actors

    def update(self):
        """Update the gamefield"""

        #update actors
        for actor in self.actors.values():

            #broadcast about new players
            if actor.newingame and actor.login_state==3:
                self.broadcast("%s joined the game.\n" % actor.name)
                self.recv(actor, "help") # show help
                actor.newingame=False

    def recv(self, actor, cmd):
        """Received command from actor"""

        if cmd=="quit":actor.client.deactivate()
        if cmd=="look":self.look(actor)
        if cmd=="help":self.showhelp(actor)
        if cmd=="status":self.showstatus(actor)
        if cmd=="map":self.showmap(actor)
        #
        actor.send_prompt()

    def broadcast(self, message):
        """broadcast message to all actors"""
        for actor in self.actors.values():
            actor.client.send_cc(message)

    def showhelp(self, actor):
        """Show help"""
        commands="help quit look status map"
        actor.client.send_cc("^gHELP:^~ Commands: %s\n" % commands)

    def look(self, actor):
        room=globalroomloader.get_room(actor.location)
        actor.client.send_cc("You are in %s - %s\n" %\
                             (str(room.name), str(room.desc)))

    def showstatus(self,actor):
        actor.client.send_cc("STATUS\n")
        actor.client.send_cc("Name: %s\n" % actor.name)

    def showmap(self,actor):
        room=globalroomloader.get_room(actor.location)
        for line in room.get_representation():
            actor.client.send_cc("".join(line)+"\n")