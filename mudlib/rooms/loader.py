from room import Room

class RoomLoader:
    def __init__(self):
        self.rooms={}

    def load_room(self,roomuuid):
        """Load room by uuid"""
        newroom=Room()
        return newroom