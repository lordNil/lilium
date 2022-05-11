
import time
import os
import random
from playsound import playsound

##-----------------------------Initialize Data---------------------------------

#### Gets data from the sounds/books folder

sex_sounds = {} # dict with folder of sex sounds, and list of items
ss = os.listdir('sound/sex')
for s in ss:
    basedir = 'sound/sex/' + s
    files = os.listdir(basedir)
    sex_sounds[s] = files

# list of wakeup sounds
wakeup_sounds = []
ww = os.listdir('sound/wakeup')
for w in ww:
    basedir = 'sound/wakeup/' + w
    wakeup_sounds.append(basedir)

# list of sleep sounds
sleep_sounds = []
ww = os.listdir('sound/sleep')
for w in ww:
    basedir = 'sound/sleep/' + w
    sleep_sounds.append(basedir)



##-----------------------------Main Function---------------------------------


def create_sound( world ):
    
    while world['power state']:

        
        if world['main state'] == 'awake':   
            # selects a random sound from list and plays it
            out = random.choice(wakeup_sounds)
            playsound(out)
            time.sleep(3)


        if world['main state'] == 'sleep':
            time.sleep(0.5)

                
        if world['main state'] == 'sex':
            # selects a random sound from list and plays it
            basedir = 'sound/sex/Oral Sex/'
            slist = sex_sounds['Oral Sex']
            out = random.choice(slist)
            out = basedir + out
            playsound(out)


        time.sleep(0.3)
    


## ---------------------- Other Functions -------------------
