
class Room:
    def __init__(self):
        self.uuid=""
        self.name=""
        self.desc=""
        #
        self.size=(32,16)
        self.places=self.makearray(self.size)
        self.warps=[] # teleport to thers locations [x,y,roomID]

    def get_representation(self,actor):
        """Return room represented in char as list of lines"""
        lines=[]
        #Create map
        for y in range(self.size[1]):
            line=[]
            for x in range(self.size[0]):
                #represent items
                if self.places[y][x]==None:line.append("-")
                else:line.append("^go^~")
            lines.append(line)
        #Draw warps on map
        for warp in self.warps:
            lines[warp[1]][warp[0]]="^go^~"
        #Draw player
        lines[actor.pos[1]][actor.pos[0]]="^B@^~"
        return lines

    def makearray(self,size):
        array=[]
        for y in range(size[1]):
            array.append([None]*size[0])
        return array