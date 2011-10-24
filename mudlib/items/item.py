
class Item:
    def __init__(self):
        self.uuid=""
        self.name=""
        self.desc=""
        #
        self.eatreghp=0 # eat regenerate hp
        self.eatregfood=0 # eat regenerate food

    def __str__(self):
        return self.name