class Monster:
    def __init__(self, uuid):
        self.uuid=uuid
        self.name=""
        self.desc=""
        self.hp=[5,5]

    def defend(self,actor):
        """Defenf against actor"""
        actor.in_fight=True
        dmg=1
        actor.send("\r^R  %s uderza cie zadajac %s obrazen^~\n" % (self.name,dmg))
        actor.hp[0]-=dmg