def decrase_water(actor, howmuch=1.0):
    actor.water-=howmuch
    if actor.water<0.0:actor.water=0.0

def decrase_food(actor, howmuch=1.0):
    actor.food-=howmuch
    if actor.food<0.0:actor.food=0.0