from mudlib.rooms import globalroomloader

def showhelp(actor):
    """Show help"""
    commands="pomoc, wyjdz, patrz, status, mapa, powiedz <text>, "
    commands+="polnoc, wschod, zachod, poludnie, online"
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
    actor.client.send_cc("  ^Y-------------------------^~\n")
    actor.client.send_cc("  ^YPozycja:^~ %s\n" % actor.pos)

def showmap(actor):
    """Show map"""
    room=globalroomloader.get_room(actor.location)
    for line in room.get_representation(actor):
        actor.client.send_cc("".join(line)+"\n")

def say(actors, actor, text):
    """Say text"""
    for act in actors:
        if act!=actor:
            act.client.send_cc("^Y%s powiedzial:^~ %s\n" % (actor.name, text))
        else:
            act.client.send_cc("^mPowiedzialesz:^~ %s\n" % (text))

def showonline(actors,actor):
    """Show online users"""
    actor.client.send_cc("Teraz gra %i graczy.\n" % len(actors))
    for online in actors:
        actor.client.send_cc("^Y"+online.name+"^~, ")
    actor.client.send_cc("\n")

def move(actor,direction):
    """move actor in direction"""
    mv={"n":(0,-1),
        "s":(0,1),
        "e":(1,0),
        "w":(-1,0),
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
        actor.pos=[nx,ny]
        showmap(actor)
        return False