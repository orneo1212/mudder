from mudlib.actions import monsters_act
from mudlib.actions import stats
from mudlib.actor import actorcommands
from mudlib.rooms import globalroomloader
from mudlib.sys.timer import Timer

class GameField:
    def __init__(self, actors):
        self.actors=actors
        self.foodtimer=Timer()
        self.watertimer=Timer()
        self.monstertimer=Timer()
        self.warrningtimer=Timer()

    def update(self):
        """Update the gamefield"""
        #update spawners
        if self.monstertimer.timepassed(1000*60):
            for actor in self.actors.values():
                monsters_act.spawn_new_monsters(actor.get_room())
        #decrase food
        if self.foodtimer.timepassed(1000*5*60):
            for actor in self.actors.values():
                stats.decrase_food(actor)
        #decrase water
        if self.watertimer.timepassed(1000*10*60):
            for actor in self.actors.values():
                stats.decrase_water(actor)
        #update warrnings
        if self.warrningtimer.timepassed(1000*2*60):
            for actor in self.actors.values():
                actor.update_warrnings()

        #update actors
        for actor in self.actors.values():

            actor.update() # update stats

            #broadcast about new players
            if actor.newingame and actor.login_state==3:
                self.broadcast("%s dolaczyl do gry.\n" % actor.name)
                #Call onenter to the room
                room=globalroomloader.get_room(actor.location)
                room.on_enter(actor)
                #look
                self.recv(actor, "look") # show info
                actor.newingame=False

    def recv(self, actor, cmd):
        """Received command from actor"""
        cmd=cmd.split()
        #parse arguments and command
        if len(cmd)>1:
            args=cmd[1:]
            cmd=cmd[0].lower()
        else:
            cmd=cmd[0].lower()
            args=[]

        #Parse commands
        if cmd in ["wyjdz", "quit"]:actor.client.deactivate()
        if cmd in ["patrz", "look", "l", "p"]:actorcommands.look(actor)
        if cmd in ["pomoc", "help", "h"]:actorcommands.showhelp(actor)
        if cmd in ["status", "st"]:actorcommands.showstatus(actor)
        if cmd in ["powiedz", "say", "~"]:
            actorcommands.say(self.actors.values(), actor, " ".join(args))
        if cmd in ["polnoc", "north", "n"]:actorcommands.move(actor, "n")
        if cmd in ["poludnie", "south", "s"]:actorcommands.move(actor, "s")
        if cmd in ["wschod", "east", "e"]:actorcommands.move(actor, "e")
        if cmd in ["zachod", "west", "w"]:actorcommands.move(actor, "w")
        if cmd in ["szukaj", "search"]:actorcommands.search(actor)
        if cmd in ["inwentarz", "inw", "inv", "inventory"]:
            actorcommands.showinventory(actor, args)
        if cmd in ["usiadz","sit"]:
            actorcommands.sit(actor)
        if cmd in ["wstan","stand"]:
            actorcommands.stand(actor)
        if cmd in ["online"]:
            actorcommands.showonline(self.actors.values(), actor)
        if cmd in ["podnies", "pickup"]:
            actorcommands.pickup(actor, args)
        if cmd in ["upusc", "drop"]:
            actorcommands.drop(actor, args)
        if cmd in ["zabij", "kill"]:
            actorcommands.fight_with_monster(actor, args)
        if cmd in ["zjedz", "jedz", "eat"]:
            actorcommands.eatfood(actor, args)
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
