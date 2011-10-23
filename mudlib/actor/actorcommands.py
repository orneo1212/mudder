from mudlib.items import globalitemloader
from mudlib.rooms import globalroomloader
import random

def showhelp(actor):
    """Show help"""
    commands="pomoc, wyjdz, patrz, status, powiedz <text>, szukaj, "
    commands+="polnoc, wschod, zachod, poludnie, online, inwentarz, "
    commands+="podnies <nazwa>, upusc <nazwa>"
    actor.client.send_cc("^gPOMOC:^~ Polecenia: %s\n" % commands)

def look(actor):
    """Show informations about room"""
    room=globalroomloader.get_room(actor.location)

    #Show exits
    actor.client.send_cc("\r[ Wyjscia: ^Y")
    for exit in room.exits:
        if exit=="n":actor.client.send_cc("polnoc ")
        elif exit=="e":actor.client.send_cc("wschod ")
        elif exit=="w":actor.client.send_cc("zachod ")
        elif exit=="s":actor.client.send_cc("poludnie ")
    actor.client.send_cc("^~ ]\n")
    #show information about location
    actor.client.send_cc("Jestes w ^g%s^~ - ^y%s^~\n" %\
                         (str(room.name), str(room.desc)))
    #show items on the ground
    if len(room.items)>0:
        if len(room.items)>1:
            actor.send("\r^G  Tu leza ")
        else:
            actor.send("\r^G  Tu lezy ")
        #enumarate items
        for item in room.items:
            itemobj=globalitemloader.get_item(item)
            actor.send(str(itemobj.name)+" ")
        actor.send("^~\n")

def showstatus(actor):
    """Show actor status"""
    actor.client.send_cc("^YSTATUS^~\n")
    actor.client.send_cc("  ^YImie:^~ %s\n" % actor.name)
    actor.client.send_cc("  ^YHP:^~ %s\n" % actor.hp)
    actor.client.send_cc("  ^YMP:^~ %s\n" % actor.mp)
    actor.client.send_cc("  ^YSila:^~ %s\n" % actor.str)
    actor.client.send_cc("  ^YInteligencja:^~ %s\n" % actor.int)
    actor.client.send_cc("  ^YWitalnosc:^~ %s\n" % actor.vit)
    actor.client.send_cc("  ^YZrecznosc:^~ %s\n" % actor.dex)
    actor.client.send_cc("  ^YJedzenie:^~ %s %%\n" % actor.food)
    actor.client.send_cc("  ^YWoda:^~ %s %%\n" % actor.water)
    #actor.client.send_cc("  ^Y-------------------------^~\n")
    #actor.client.send_cc("  ^YPozycja:^~ %s\n" % actor.pos)

def say(actors, actor, text):
    """Say text"""
    for act in actors:
        if act!=actor:
            act.client.send_cc("^Y\r%s powiedzial:^~ %s\n" % (actor.name, text))
        else:
            act.client.send_cc("^m\rPowiedziales:^~ %s\n" % (text))

def showonline(actors, actor):
    """Show online users"""
    actor.client.send_cc("Teraz gra %i graczy.\n" % len(actors))
    for online in actors:
        actor.client.send_cc("^Y"+online.name+"^~, ")
    actor.client.send_cc("\n")

def move(actor, direction):
    """move actor in direction"""

    room=globalroomloader.get_room(actor.location)

    err=0

    if direction not in room.exits.keys():err=1

    if err:
        actor.client.send_cc("^rNie mozesz isc w tym kierunku.^~\n")
        return True
    else:
        actor.location=room.exits[direction]
        look(actor)
        return False

def showinventory(actor, args):
    """Show actor inventory"""
    if len(actor.inventory)==0:
        actor.client.send_cc("\r^gNic nie masz w plecaku^~\n")
        return
    actor.client.send_cc("^Y\rZawartosc twojego plecaka^~\n")

    tmpinv=[]
    for item in actor.inventory[:]:
        if item in tmpinv:continue
        itemobj=globalitemloader.get_item(item)
        actor.client.send_cc("\r  "+str(itemobj.name)+" x %s\n" % actor.inventory.count(item))
        tmpinv.append(item)

def search(actor):
    """Search for item on the ground"""
    items=[
           #itemuuid, chance
           ["001", 1],
           ["002", 30],
           ]
    item=random.choice(items)
    number=random.randint(0, 100)
    if number<=item[1] and not actor.found_item:
        actor.found_item=True # Actor found item in this area
        #create object
        itemobj=globalitemloader.get_item(item[0])
        actor.client.send_cc("^G\rZnalazles %s^~\n" % itemobj.name)
        actor.inventory.append(item[0])
    else:actor.client.send_cc("^R\rNic nie znalazles^~\n")

def pickup(actor,args):
    """pickup item from ground"""
    if len(args)==0:
        actor.send("\r^rPodniesc co?^~\n")
        return

    args=" ".join(args)
    room=globalroomloader.get_room(actor.location)

    for item in room.items:
        itemobj=globalitemloader.get_item(item)
        if args.lower() in itemobj.name.lower():
            actor.send("\r^gPodnosisz %s.^~\n" % itemobj.name)
            actor.inventory.append(item)
            room.items.remove(item)
            return
    #there no item with given part of name
    actor.send("\r^rNie lezy tu nic o podanej nazwie.^~\n")

def drop(actor,args):
    """drop item into ground"""
    if len(args)==0:
        actor.send("\r^rUpuscic co?^~\n")
        return

    args=" ".join(args)
    room=globalroomloader.get_room(actor.location)

    for item in actor.inventory:
        itemobj=globalitemloader.get_item(item)
        if args.lower() in itemobj.name.lower():
            actor.inventory.remove(item)
            room.items.append(item)
            actor.send("\r^gWyrzucilesz %s^~\n" % itemobj.name)
            return
    #there no item with given part of name
    actor.send("\r^rNie masz nic o podanej nazwie.^~\n")
