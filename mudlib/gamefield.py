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

    def unloaddata(self):
        """Unload data"""
        for actor in self.actors:
            actor.savedata()

    def broadcast(self, message):
        """broadcast message to all actors"""
        for actor in self.actors.values():
            actor.client.send_cc(message)

    def showhelp(self, actor):
        """Show help"""
        commands="help quit look status map"
        actor.client.send_cc("^gHELP:^~ Commands: %s\n" % commands)

    def look(self, actor):
        """Show informations about room"""
        room=globalroomloader.get_room(actor.location)
        actor.client.send_cc("You are in ^g%s^~ - ^y%s^~\n" %\
                             (str(room.name), str(room.desc)))

    def showstatus(self,actor):
        """Show actor status"""
        actor.client.send_cc("STATUS\n")
        actor.client.send_cc("  Name: %s\n" % actor.name)
        actor.client.send_cc("  HP: %s\n" % actor.hp)
        actor.client.send_cc("  MP: %s\n" % actor.mp)
        actor.client.send_cc("  Strength: %s\n" % actor.str)
        actor.client.send_cc("  Inteligence: %s\n" % actor.int)
        actor.client.send_cc("  Vitality: %s\n" % actor.vit)
        actor.client.send_cc("  Dexterity: %s\n" % actor.dex)

    def showmap(self,actor):
        """Show map"""
        room=globalroomloader.get_room(actor.location)
        for line in room.get_representation():
            actor.client.send_cc("".join(line)+"\n")