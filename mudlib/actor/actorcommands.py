from mudlib.rooms import globalroomloader

def showhelp(actor):
    """Show help"""
    commands="help quit look status map"
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

def showmap(actor):
    """Show map"""
    room=globalroomloader.get_room(actor.location)
    for line in room.get_representation(actor):
        actor.client.send_cc("".join(line)+"\n")

def say(actors, actor,text):
    for act in actors:
        if act!=actor:
            act.client.send_cc("^Y%s say:^~%s" % (actor.name,text))
        else:
            act.client.send_cc("^mYou say:^~%s" % (text))