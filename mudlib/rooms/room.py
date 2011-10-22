
class Room:
    def __init__(self):
        self.uuid=""
        self.name=""
        self.desc=""
        #
        self.places=self.makearray((32,32))

    def makearray(self,size):
        array=[]
        for y in range(size[1]):
            array.append([None]*size[0])
        return array