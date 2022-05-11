import time
import subprocess
import multiprocessing as MP
import random


# -------- Processes that are started -------------

def UI(world):
    print('Started UI Module')
    import ui as U
    U.create_window(world) 

def Motion(world):
    print('Started Motion Module')
    import motion as M
    M.create_motion(world)
    print('Shutdown motors')

def Sound(world):
    print('Started Sound Module')
    import sound as S
    S.create_sound(world)
    print('Shutdown Sound')

def Vision(world):
    print('Starting Vision Module')
    import vision as V
    V.create_vision(world)
    print('shutdown vision')


#----------------- Main Function ---------------

if __name__ == '__main__':
    # On Windows calling this function is necessary.
    MP.freeze_support()
    
    # initialize world data object
    mgr = MP.Manager()
    world = mgr.dict()

    #  Basic States
    world[ 'power state' ] = 1   # Options: 1, 0
    world[ 'main state']   = 'startup'    # options are: startup, sleep, wakeup, awake, talking, sex, shutdown
    world[ 'mic state' ]   = 'search'  # Options: 'connected', 'disconencted', 'search', 'test', 'wait'
    world[ 'speaker state']= 'wait'    # options 'wait', 'sex'
    world[ 'vision state'] = 'disconnected'  # 
    world[ 'motion state'] = 'disconnected'  # 
    world[ 'web state']    = 'disconnected'
    world[ 'head motion']  = 'random'  # options are relax, random, search, target, yes, no, sex
    world[ 'sex state']    = 'Playful'  #
    # Ports to connect Sensors
    world[ 'motor port']   = 'COM7'  # Motor port usually something like COM4 or ttyS1
    world[ 'mic port']     = 1  
    world[ 'speaker port'] = 3
    world[ 'camera port']  = 0
    # Data Objects
    world[ 'volume']     = 0.2 # 
    world[ 'motors']     =  []   # Contains data of all the motors
    world[ 'move'  ]     =  []   # command to move motors. list of [ID, Goal_pos]
    world[ 'L eye']      =  []   # Left eye image as a Cv2 Frame
    world[ 'R eye']      =  []   # Right eye image as a CV2 Frame
    world[ 'L faces']    =  []   # detected faces from left eye
    world[ 'R faces']    =  []
    world[ 'sex bar']    = 10    # progress bar from 0-100 for sex
    world[ 'sex sounds'] = {}
    world[ 'sex voice']  = 'Oral Sex' # the voice for the sex sounds (may be '')
    world[ 'start convo']= False      # if true the android will try to start a conversation. 

    p1 = MP.Process(target=UI,     args=(world,))
    p2 = MP.Process(target=Motion, args=(world,))
    p3 = MP.Process(target=Sound,  args=(world,))
    p4 = MP.Process(target=Vision, args=(world,))


    Process_list = [ p1, p2, p3, p4]

    for p in Process_list:
        p.start()
    for p in Process_list:
        p.join()
    



