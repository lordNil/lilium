
import cv2
import time
import numpy as np


##--------------------------Main Function-----------------------------------

def create_vision( world ):

    while world['power state']:


        if world['vision state'] == 'disconnected':
            try:
                result = init_camera(world['camera port'])
                if result:
                    print('cammera connected')
                    world['vision state'] = 'connected'
            except Exception as e:
                print('camera connection failed')
                print(e)



        if world['vision state'] =='connected' and world['main state']=='awake':
            try:
                a, b = snapshot()
                save('test.jpg', a)
                time.sleep(0.5)
            except:
                print('could not take picture')
            
            
    
    
            
        time.sleep(0.2)
    release_camera()


##---------------------------------------------------------------------------------



def init_camera( cam_num ):
    result = True           
    
    if result:

        global cap
        cap = cv2.VideoCapture( cam_num, cv2.CAP_DSHOW )
        # resolutions for dual camera are 2560 x 720, 1280x720, 1280x480, 640x480, 640x240
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        #init_FR()

    return result


## takes a picture, returns picture data
## often camera has a startup time and first few pics are bad
# returns left and right images (from perspective of robot)
def snapshot():
    ret, frame = cap.read()
    if ret==True:
        #print(" sucess in image capture ")
        #frame = cv2.transpose( frame )
        frame = cv2.flip( frame, flipCode=0 )  # rotate on x axis
        frame = cv2.flip( frame, flipCode=1 )  # rotate on y axis
        width = frame.shape[1]
        width_cut = width //2
        A = frame[:, :width_cut]
        B = frame[:, width_cut:]
        
        return A , B
    else:
        print(" failed in image capture ")



def release_camera():
    global cap
    cap.release()

def save( name , img ):
    boo = cv2.imwrite( name , img )
    return boo

def list_cameras():
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    """
    non_working_ports = []
    dev_port = 0
    working_ports = []
    available_ports = []
    while len(non_working_ports) < 6: # if there are more than 5 non working ports stop the testing.
        print('testing camera port: '+ str(dev_port))
        camera = cv2.VideoCapture(dev_port, cv2.CAP_DSHOW)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
            print("Port %s is not working." %dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(6)
            if is_reading:
                print("Camera Port %s " %(dev_port))
                print(' is working ')
                working_ports.append(dev_port)
            else:
                print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                available_ports.append(dev_port)
        dev_port +=1
    return working_ports


########### test code

if __name__ == '__main__':
    list_cameras()

  