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
        #parse arguments and command
        if len(cmd)>1:
            args=cmd[1:]
            cmd=cmd[0]
        else:
            cmd=cmd[0]
            args=[]

        #Parse commands
        if cmd=="quit":actor.client.deactivate()
        if cmd in ["look","l"]:actorcommands.look(actor)
        if cmd in ["help","h"]:actorcommands.showhelp(actor)
        if cmd in ["status","st"]:actorcommands.showstatus(actor)
        if cmd in ["map"]:actorcommands.showmap(actor)
        if cmd in ["say","~"]:actorcommands.say(self.actors.values(), actor, " ".join(args))
        if cmd in ["north","n"]:actorcommands.move(actor, "n")
        if cmd in ["south","s"]:actorcommands.move(actor, "s")
        if cmd in ["east","e"]:actorcommands.move(actor, "e")
        if cmd in ["west","w"]:actorcommands.move(actor, "w")
        if cmd in ["online"]:actorcommands.showonline(self.actors.values(),actor)
        #
        actor.send_prompt()

    def unloaddata(self):
        """Unload data"""
        for actor in self.actors.values():
            actor.savedata()

    def broadcast(self, message):
        """broadcast message to all actors"""
        for actor in self.actors.values():
            actor.client.send_cc(message)
