
class Room:
    def __init__(self):
        self.uuid=""
        self.name=""
        self.desc=""
        #
        self.size=(32,16)
        self.places=self.makearray(self.size)

    def get_representation(self,actor):
        """Return room represented in char as list of lines"""
        lines=[]
        for y in range(self.size[1]):
            line=[]
            for x in range(self.size[0]):
                #Represent player
                if x==actor.pos[0] and y==actor.pos[1]:
                    line.append("^B@^~")
                    continue
                #represent items
                if self.places[y][x]==None:line.append("-")
                else:line.append("^go^~")
            lines.append(line)
        return lines

    def makearray(self,size):
        array=[]
        for y in range(size[1]):
            array.append([None]*size[0])
        return array