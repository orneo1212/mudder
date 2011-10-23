from mudlib.rooms import globalroomloader

def showhelp(actor):
    """Show help"""
    commands="help, quit, look, status, map, say <text>"
    actor.client.send_cc("^gHELP:^~ Commands: %s\n" % commands)

def look(actor):
    """Show informations about room"""
    room=globalroomloader.get_room(actor.location)
    actor.client.send_cc("You are in ^g%s^~ - ^y%s^~\n" %\
                         (str(room.name), str(room.desc)))

def showstatus(actor):
    """Show actor status"""
    actor.client.send_cc("^YSTATUS^~\n")
    actor.client.send_cc("  ^YName:^~ %s\n" % actor.name)
    actor.client.send_cc("  ^YHP:^~ %s\n" % actor.hp)
    actor.client.send_cc("  ^YMP:^~ %s\n" % actor.mp)
    actor.client.send_cc("  ^YStrength:^~ %s\n" % actor.str)
    actor.client.send_cc("  ^YInteligence:^~ %s\n" % actor.int)
    actor.client.send_cc("  ^YVitality:^~ %s\n" % actor.vit)
    actor.client.send_cc("  ^YDexterity:^~ %s\n" % actor.dex)
    actor.client.send_cc("  ^Y-------------------------^~\n")
    actor.client.send_cc("  ^YPosition:^~ %s\n" % actor.pos)

def showmap(actor):
    """Show map"""
    room=globalroomloader.get_room(actor.location)
    for line in room.get_representation(actor):
        actor.client.send_cc("".join(line)+"\n")

def say(actors, actor, text):
    """Say text"""
    for act in actors:
        if act!=actor:
            act.client.send_cc("^Y%s say:^~ %s\n" % (actor.name, text))
        else:
            act.client.send_cc("^mYou say:^~ %s\n" % (text))

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
        actor.client.send_cc("^rYou can't go there.^~\n")
        return True
    else:
        actor.pos=[nx,ny]
        return False