#!/usr/bin/env python
from miniboa import TelnetServer
from mudlib.actor.actor import Actor
from mudlib.gamefield import GameField
from mudlib.sys.login import Login
import mudlib
import os

#GLOBAL PATH
mudlib.rootpath=os.path.dirname(__file__)

class MudderServer:
    def __init__(self):
        self.port=7777
        #server object
        self.server=TelnetServer(self.port,
            "",
            self.onconnect,
            self.ondisconnect,
            .05)
        #clients (TelnetClient)
        self.clients=[]
        self.actors={} # mudlib actors key:fileno value:actor
        #Gamefield
        self.gamefield=GameField(self.actors)
        #Server state
        self.running=True

    def onconnect(self, client):
        client.send_cc("Witaj...\n")
        client.send_cc("Wprowadz imie:")
        client.request_terminal_type()
        #add client
        self.actors[client.fileno]=Actor(client)
        self.actors[client.fileno].onconnect()
        self.clients.append(client)
        print "++ User connected from %s" % str(client.address)

    def ondisconnect(self, client):
        self.actors[client.fileno].ondisconnect()
        self.actors.pop(client.fileno)
        self.clients.remove(client)
        print "-- User disconnected from %s" % str(client.address)

    def processclient(self):
        """Process client"""

        for client in self.clients:
            #Get actor reresented by connection
            actor=self.actors[client.fileno]
            if actor.login_state==4:client.deactivate()
            #if someone send message
            if client.active and client.cmd_ready:
                #get command
                cmd=client.get_command()
                if cmd=="":continue # skip empty messages
                #print "DD", client.address, cmd
                #If not logged in
                if actor.login_state!=3:
                    Login(actor, cmd) # do login
                #logged in send command to gamefield
                else:self.gamefield.recv(actor, cmd)

    def serverloop(self):
        print "Server started at port %s" % str(self.port)
        try:
            while self.running:
                self.server.poll()
                self.processclient()
                self.gamefield.update()
        except KeyboardInterrupt,e:self.onexit(e)

    def onexit(self, error):
        print "\rStopping Server..."
        print error
        #Unload data
        self.gamefield.unloaddata()
        exit(1)

if __name__=="__main__":
    ss=MudderServer()
    ss.serverloop()
