from loaders import get_actors_files_list

def Login(actor, command):
    # no name specified
    if actor.login_state==0:
        correct=check_name(actor, command)
        if correct: # if name correct
            exist=actor_exist(actor, command)
            #Existing actor
            if exist:
                actor.name=command
                actor.loaddata()
                actor.login_state=1
                actor.client.send_cc("^gPostac istnieje.^~\nPodaj swoje haslo:")
                actor.client.password_mode_on()
            #New actor
            else:
                actor.name=command
                actor.loaddata()
                actor.login_state=2
                actor.client.send_cc("\rPostac nie istnieje. Podaj haslo dla nowej postaci:")
                actor.client.password_mode_on()
        else:actor.client.send_cc("^rZle imie.^~ Wprowadz nowe:")

    # password not specified
    elif actor.login_state==1:
        correct=check_password(actor, command)
        if correct: # if password correct
            actor.client.password_mode_off()
            actor.client.send_cc("^g\nLogowanie powiodlo sie.^~\n")
            actor.login_state=3 # login success
        else:
            actor.client.send_cc("^r\nZle haslo.^~\n")
            actor.login_state=4 # Failed disconnect on poll

    # New character
    elif actor.login_state==2:
        actor.password=command
        actor.client.password_mode_off()
        actor.client.send_cc("^g\nPostac stworzona.^~\n")
        actor.login_state=3 # Logged in

def check_name(actor, name):
    """Return True if actor can use that name. (correct syntax)"""
    if len(name)>3 and len(name)<=20 and " " not in name:
        return True
    else:return False

def actor_exist(actor,name):
    """Return True if actor with given name exist"""
    if name+".json" in get_actors_files_list():return True
    return False

def check_password(actor, password):
    """Return True if password match"""
    if password==actor.password:return True
    else:return False