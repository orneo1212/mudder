from mudlib.items import globalitemloader
import random

class Monster:
    def __init__(self, uuid):
        self.uuid=uuid
        self.name=""
        self.desc=""
        self.hp=[5, 5]
        self.stats=[] # [attack,defence, speed]
        self.exp=0 # how much exp actor gain when monster die
        self.drop=[] # Drop list [chance, itemuuid, maxdropcount]

    def defend(self, actor):
        """Defenf against actor"""
        #Prepare fight
        actor.in_fight=True
        actor.target=self
        actor.sit=False

        texts_atk=[
                   "^G\r zadajesz %s obrazen.^~\n",
                   "^G\r po wycelowaniu udalo ci sie zranic go odejmujac mu %s zycia.^~\n",
                   ]

        texts_dead=[
                    "^G\r i po tym uderzeniu %s pada martwy na ziemie.^~\n",
                    "^G\r po kilku chwilach juz nie ma kogo zabic. %s nie zyje.^~\n",
                    ]

        texts_dodge=[
                    "^G\r Pudlo.. %s nie dostal. Ktos mowil ze bedzie latwo?^~\n",
                    "^G\r bylo blisko jednak %s byl szybszy.^~\n",
                    ]

        #calculate dodge
        dodge=float(actor.dex)/float(self.stats[2])
        dodge+=random.randint(-2, 2)
        dodge=dodge<0

        #decrase actor food
        actor.food-=0.1

        if not dodge:
            #Calculate actor damange
            dmg=float(actor.str)/float(self.stats[1])*actor.str
            dmg=int(dmg)
            dmg+=random.randint(-5, 5)
            if dmg<0:dmg=0

            #decrase hp
            print self.hp
            self.hp[0]-=dmg
            #show actor attack message
            text=random.choice(texts_atk)
            actor.send(text % dmg)
            #check monster dead
            if self.hp[0]<=0:
                #monster die
                text=random.choice(texts_dead)
                actor.send(text % self.name)
                actor.in_fight=False
                actor.target=None
                #add drop
                self.give_drop(actor)
                #remove monster from location
                room=actor.get_room()
                if self in room.monsters:room.monsters.remove(self)
                #add experiance
                actor.exp[0]+=self.exp
                actor.send("^G\rOtrzymalesz %s doswiadczenia.^~\n" % self.exp)
                actor.send_prompt()
        #Dodge
        else:
            text=random.choice(texts_dodge)
            actor.send(text % self.name)

    def give_drop(self, actor):
        """give drop items"""
        if len(self.drop)==0:return
        drop=random.choice(self.drop)
        count=random.randint(1, drop[2])
        #if chance
        if random.randint(0, 100)<=drop[0]:
            for coun in range(count):
                actor.inventory.append(drop[1])
            item=globalitemloader.get_item(drop[1])
            actor.send("^y\rOtrzymujesz %s x %s.^~\n" % (item.name, count))