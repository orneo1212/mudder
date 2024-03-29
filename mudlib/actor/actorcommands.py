from mudlib.items import globalitemloader
from mudlib.rooms import globalroomloader
import random

def showhelp(actor):
    """Show help"""
    actor.client.send_cc("^gPolecenia:\n")
    #commadns listing
    commands="pomoc, patrz [naco], status, online "
    actor.send("^Y\rInformacje:^~ %s\n" % commands)
    #
    commands="polnoc, wschod, zachod, poludnie, usiadz, wstan"
    actor.send("^Y\rPoruszanie:^~ %s\n" % commands)
    #
    commands="podnies <nazwa>, upusc <nazwa>, szukaj, inwentarz, zjedz <nazwa>, daj <komu> <co> "
    actor.send("^Y\rPrzedmioty:^~ %s\n" % commands)
    #
    commands="powiedz <tekst>"
    actor.send("^Y\rRozmowa:^~ %s\n" % commands)
    #
    commands="zabij <kogo>"
    actor.send("^Y\rWalka:^~ %s\n" % commands)
    #
    commands="wyjdz "
    actor.send("^Y\rInne:^~ %s\n" % commands)

def look(actor, args=[]):
    """Show informations about room"""
    room=actor.get_room()

    #If argument given then search for matching item/place and show desc
    if len(args)>0:
        args=" ".join(args)
        #Check items on the ground
        item=room.get_item_by_name(args)
        if item:
            actor.send("\r^y%s^~\n" % item.name)
            actor.send("\r  %s\n" % item.desc)
            return
        #check items from inventory
        item=actor.get_item_by_name(args)
        if item:
            actor.send("\r^y%s^~\n" % item.name)
            actor.send("\r  %s\n" % item.desc)
            return
        #Check monsters in room
        monster=room.get_monster_by_name(args)
        if monster:
            actor.send("\r^y%s^~\n" % monster.name)
            actor.send("\r  %s\n" % monster.desc)
            return
        return
    #########################
    #show information about location
    #########################
    actor.client.send_cc("\r^c%s^~\n" % str(room.name))
    #Show exits
    actor.client.send_cc("\r[ Wyjscia: ^Y")
    for exit in room.exits:
        if exit=="n":actor.client.send_cc("polnoc ")
        elif exit=="e":actor.client.send_cc("wschod ")
        elif exit=="w":actor.client.send_cc("zachod ")
        elif exit=="s":actor.client.send_cc("poludnie ")
    actor.client.send_cc("^~ ]\n")
    #show desc about location
    actor.client.send_cc("%s\n" % str(room.desc))
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
    #Show information about players in actor room
    if len(room.players)>1:
        actor.send("\r^wSa tutaj inni gracze: ")
        for player in room.players:
            if player!=actor:
                actor.send("^Y%s^~ " % player.name)
        actor.send("^~\n")
    #Show information about monsters in actor room
    if len(room.monsters)>0:
        actor.send("\r^RTutaj sa wrogie potwory. Badz ostrozny: ")
        for monster in room.monsters: # for each monster object in room
            #if last dont add comma
            if monster==room.monsters[-1]:
                actor.send("%s" % str(monster.name))
            else:
                actor.send("%s, " % str(monster.name))
        actor.send("^~\n")

def showstatus(actor):
    """Show actor status"""
    actor.client.send_cc("^YSTATUS^~\n")
    actor.client.send_cc("  ^BImie:^~ %s\n" % actor.name)
    actor.client.send_cc("  ^BPoziom:^~ %s\n" % actor.level)
    actor.client.send_cc("  ^BDoswiadczenie:^~ %s\n" % actor.exp)
    actor.client.send_cc("  ^BZycie:^~ %s/%s\n" % (actor.hp[0], actor.hp[1]))
    actor.client.send_cc("  ^BMana:^~ %s/%s\n" % (actor.mp[0], actor.mp[1]))
    actor.client.send_cc("  ^BSila:^~ %s\n" % actor.str)
    actor.client.send_cc("  ^BInteligencja:^~ %s\n" % actor.int)
    actor.client.send_cc("  ^BWitalnosc:^~ %s\n" % actor.vit)
    actor.client.send_cc("  ^BZrecznosc:^~ %s\n" % actor.dex)
    actor.client.send_cc("  ^BJedzenie:^~ %s %%\n" % int(actor.food))
    actor.client.send_cc("  ^BWoda:^~ %s %%\n" % int(actor.water))
    #actor.client.send_cc("  ^Y-------------------------^~\n")

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
    #you can't move if siting
    if actor.sit:
        actor.send("\r^rMoze jeszcze na siedzaco mam skakac?^~\n")
        return
    room=actor.get_room()

    err=0

    if direction not in room.exits.keys():err=1

    if err:
        actor.client.send_cc("^rNie mozesz isc w tym kierunku.^~\n")
        return True
    else:
        actor.found_item=False
        actor.water-=0.1 # decrease water
        #Update actor location
        actor.moveto(room.exits[direction])
        look(actor)
        return False

def showinventory(actor, args):
    """Show actor inventory"""
    if len(actor.inventory)==0:
        actor.client.send_cc("\r^gNic nie masz w plecaku.^~\n")
        return
    actor.client.send_cc("^Y\rZawartosc twojego plecaka:^~\n")

    tmpinv=[]
    for item in actor.inventory[:]:
        if item in tmpinv:continue
        itemobj=globalitemloader.get_item(item)
        actor.client.send_cc("\r  "+str(itemobj.name)+" x %s\n" % actor.inventory.count(item))
        tmpinv.append(item)

def search(actor):
    """Search for item on the ground"""
    room=actor.get_room()

    if len(room.searchitems)>0:
        item=random.choice(room.searchitems) # get random item
    else:item=["", -1] # 0% chance to find (if cant find any item in this loc)

    number=random.randint(0, 100)
    if number<=item[1] and not actor.found_item:
        actor.found_item=True # Actor found item in this area
        #create object
        itemobj=globalitemloader.get_item(item[0])
        actor.client.send_cc("^G\rZnalazles %s^~\n" % itemobj.name)
        actor.inventory.append(item[0])
    else:actor.client.send_cc("^R\rNic nie znalazles^~\n")

def pickup(actor, args):
    """pickup item from ground"""
    if len(args)==0:
        actor.send("\r^rPodniesc co?^~\n")
        return

    args=" ".join(args)
    room=room=actor.get_room()

    itemobj=room.get_item_by_name(args)
    if itemobj:
        actor.send("\r^gPodnosisz %s.^~\n" % itemobj.name)
        actor.inventory.append(itemobj.uuid)
        room.items.remove(itemobj.uuid)
        return
    #there no item with given part of name
    actor.send("\r^rNie lezy tu nic o podanej nazwie.^~\n")

def drop(actor, args):
    """drop item into ground"""
    if len(args)==0:
        actor.send("\r^rUpuscic co?^~\n")
        return

    args=" ".join(args)
    room=actor.get_room()

    itemobj=actor.get_item_by_name(args)
    if itemobj:
        actor.inventory.remove(itemobj.uuid)
        room.items.append(itemobj.uuid)
        actor.send("\r^gWyrzuciles %s^~\n" % itemobj.name)
        room.broadcast("\r^g%s wyrzucil %s^~\n" % (actor.name, itemobj.name), actor)
        return
    #there no item with given part of name
    actor.send("\r^rNie masz nic o podanej nazwie.^~\n")

def fight_with_monster(actor, args):
    """Fight with monster by given name"""
    room=actor.get_room()
    #you can't fight if siting
    if actor.sit:
        actor.send("\r^rMyslisz co robisz? Siedzisz i chcesz walczyc?^~\n")
        return
    #arg required
    if len(args)==0:
        actor.send("\r^rZabic kogo?^~\n")
        return
    if len(room.monsters)==0:
        actor.send("\r^rTu nie ma kogo zabijac.^~\n")
        return

    args=" ".join(args)

    monster=room.get_monster_by_name(args)
    if monster:
        actor.target=monster
        monster.defend(actor) # moster start defending
        return
    actor.send("^R\r Nie ma tutaj potwora o podanej nazwie.^~\n")

def eatfood(actor, args):
    """Eat food"""
    if len(args)==0:
        actor.send("\r^rZjesc co?^~\n")
        return

    args=" ".join(args)

    itemobj=actor.get_item_by_name(args)
    if itemobj:
        done=False
        #hp
        if itemobj.eatreghp:
            actor.send("^G\rMniam..^~\n")
            actor.hp[0]+=itemobj.eatreghp
            done=True
        #food
        if itemobj.eatregfood:
            actor.send("^G\rMniam..^~\n")
            actor.food+=itemobj.eatregfood
            done=True
        #if added stats return
        if done:
            actor.inventory.remove(itemobj.uuid)
            return
    actor.send("^r\rNie masz zjadliwej rzeczu o podanej nazwie^~\n")
    return

def sit(actor):
    """Sit down"""
    if not actor.sit:
        actor.send("\r^gSiadasz wygodnie.^~\n")
        actor.sit=True
    else:actor.send("\r^rSiedzisz juz.^~\n")

def stand(actor):
    """Stand up"""
    if actor.sit:
        actor.send("\r^gWstajesz.^~\n")
        actor.sit=False
    else:actor.send("\r^rStoisz juz.^~\n")

def give_item(actor, args):
    """Send item to other actor by name. <actorName> <itemName>"""
    #check argument
    if len(args)==0:
        actor.send("\r^rKomu chcesz dac przedmiot?^~\n")
        return
    #Check second argument
    elif len(args)==1:
        actor.send("\r^rJaki przedmiot chcesz dac?^~\n")
        return
    #Get player by name from room
    room=actor.get_room()
    newactor=room.get_actor_by_name(args[0])
    if not newactor:
        actor.send("\r^rNie ma tu gracza o podanej nazwie.^~\n")
        return
    #Get item from inventory
    item=actor.get_item_by_name(" ".join(args[1:]))
    if not item:
        actor.send("\r^rNie masz przedmiotu o podanej nazwie.^~\n")
        return
    #Finally do trade
    actor.inventory.remove(item.uuid)
    newactor.inventory.append(item.uuid)
    actor.send("\r^G^y%s^G orzymal od ciebie %s.^~\n" % (newactor.name, item.name))
    newactor.send("\r^G^y%s^G dal ci %s.^~\n" % (actor.name, item.name))