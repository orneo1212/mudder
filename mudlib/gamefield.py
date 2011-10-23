from mudlib.actor import actorcommands

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
        cmd=cmd.split()
        if len(cmd)>1:
            args=cmd[1:]
            cmd=cmd[0]
        else:
            cmd=cmd[0]
            args=[]

        if cmd=="quit":actor.client.deactivate()
        if cmd=="look":actorcommands.look(actor)
        if cmd=="help":actorcommands.showhelp(actor)
        if cmd=="status":actorcommands.showstatus(actor)
        if cmd=="map":actorcommands.showmap(actor)
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