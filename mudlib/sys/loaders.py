import os

def get_actors_files_list():
    """Return list of actors names (filenames)"""
    result=[]
    files=os.listdir("data/players/")
    for f in files:
        if f.endswith(".json"):result.append(f)
    return result

def get_rooms_files_list():
    """Return list of rooms names (filenames)"""
    result=[]
    files=os.listdir("data/rooms/")
    for f in files:
        if f.endswith(".json"):result.append(f)
    return result

def get_items_files_list():
    """Return list of items names (filenames)"""
    result=[]
    files=os.listdir("data/items/")
    for f in files:
        if f.endswith(".json"):result.append(f)
    return result