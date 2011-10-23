from mudlib.items import globalitemloader
from mudlib.rooms import globalroomloader
import random

def showhelp(actor):
    """Show help"""
    commands="pomoc, wyjdz, patrz, status, mapa, powiedz <text>, "
    commands+="polnoc, wschod, zachod, poludnie, online, inwentarz, szukaj, "
    commands+="wejdz, "
    actor.client.send_cc("^gPOMOC:^~ Polecenia: %s\n" % commands)

def look(actor):
    """Show informations about room"""
    room=globalroomloader.get_room(actor.location)
    actor.client.send_cc("Jestes w ^g%s^~ - ^y%s^~\n" %\
                         (str(room.name), str(room.desc)))

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
    #actor.client.send_cc("  ^Y-------------------------^~\n")
    #actor.client.send_cc("  ^YPozycja:^~ %s\n" % actor.pos)

def showmap(actor):
    """Show map"""
    room=globalroomloader.get_room(actor.location)
    actor.client.send_cc("\r^Y============================^~\n")
    actor.client.send_cc("\r^Y%s^~\n" % room.name)
    actor.client.send_cc("\r^Y============================^~\n")
    for line in room.get_representation(actor):
        actor.client.send_cc("\r"+"".join(line)+"\n")

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
    mv={"n":(0, -1),
        "s":(0, 1),
        "e":(1, 0),
        "w":(-1, 0),
        }
    if direction not in mv:return 1

    room=globalroomloader.get_room(actor.location)

    err=0

    nx=actor.pos[0]+mv[direction][0]
    ny=actor.pos[1]+mv[direction][1]

    if nx <0 or ny<0 or nx>room.size[0]-1 or ny>room.size[1]-1:err=1 #cannot move

    if err:
        actor.client.send_cc("^rNie mozesz isc tam.^~\n")
        return True
    else:
        actor.pos=[nx, ny]
        showmap(actor)
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
        actor.client.send_cc("\r"+str(itemobj.name)+" x %s\n" % actor.inventory.count(item))
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

def enterlocation(actor):
    room=globalroomloader.get_room(actor.location)
    #warp [posx,posy,locationUUID,destX,destY]
    for warp in room.warps:
        if actor.pos[0]==warp[0] and actor.pos[1]==warp[1]:
            actor.location=warp[2]
            actor.client.send_cc("^g\rWchodzisz.^~\n")
            actor.pos=[warp[3],warp[4]]
            actor.found_item=False
            showmap(actor)
            look(actor)
            return
    #not on warp
    actor.client.send_cc("^r\rTu nie ma zadnego wejscia.^~\n")