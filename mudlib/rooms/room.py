
class Room:
    def __init__(self):
        self.uuid=""
        self.name=""
        self.desc=""
        #
        self.exits={} # Exits
        self.items=["001"] # Items on the ground