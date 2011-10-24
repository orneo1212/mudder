from mudlib.monsters import globalmonsterloader
import random

def spawn_new_monsters(room):
    """Spawn new monsters in location"""
    if len(room.monsters)>4:return
    if len(room.possible_monsters)==0:return
    #spawn to max monsters
    for i in range(5-len(room.monsters)):
        randommonsterid=random.choice(room.possible_monsters)
        newmonster=globalmonsterloader.get_monster(randommonsterid)
        room.monsters.append(newmonster)