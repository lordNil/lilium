####### Initialization  #############
import os
import time
import random
import serial
import glob
import sys
from Motion.servos import packet_handler, port_handler                 # Uses SCServo SDK library located in servos folder

#---------------Settings and variables ------------------

SCS_ID                  = 1                 # Servo ID for testing
BAUDRATE                = 1000000           # SCServo default baudrate : 1000000
speed_limit             = 200

# Register Adresses for motors
torque       = 40    # torque enable - 1 or 0 (also write 128 here to set motor to mid position)
goal_acc     = 41    # goal acceleration
goal_pos     = 42    # goal position
goal_speed   = 46    # goal speed  (in position values / second)
curr_pos     = 56    # current position
curr_load    = 60    # current PWM 
curr_curr    = 69    # current Current up to 3.5A
packID       = 0

# Communication Result
COMM_SUCCESS = 0  # tx or rx packet communication success
COMM_PORT_BUSY = -1  # Port is busy (in use)
COMM_TX_FAIL = -2  # Failed transmit instruction packet
COMM_RX_FAIL = -3  # Failed get status packet
COMM_TX_ERROR = -4  # Incorrect instruction packet
COMM_RX_WAITING = -5  # Now recieving status packet
COMM_RX_TIMEOUT = -6  # There is no status packet
COMM_RX_CORRUPT = -7  # Incorrect status packet
COMM_NOT_AVAILABLE = -9  #


# ------------------ Motor Data --------------------------------------
# the servos are organized as a list of sevos, and each servo is a list of data
# Each servo has an ID which is it's name. You write/read its registers to control the motor.  
# left and right are from perspective of robot. (abbreviated as L and R) looking down
# clockwise and counterclockwise abbreviated as CW and CCW

servoname ="Test Motor" # describes servo motion going from limit B to A
ID      = 0              # the ID number of the servo
typee   = 0              # 0 is for sms or sts and 1 is for scs
limitA  = 100            # limits of servo position (moving in direction)
limitB  = 1000
mid     = 500           # The middle position of the motion
direct  = -1            # direction: position value goes up or down with motion ( 1 or -1)
enable  =  0            # If motor torque is enabled/disabled (1 for enable)
pos     = -1            # current position (if not known then -1)
load    = -1            # current load   (if not known then -1)

# The data table for each of the motors.
# Index:    0            1     2      3       4         5        6      7       8     9
m0  = [  servoname     , ID, typee, limitA, limitB,       mid, direct,enable, pos, load ]
m1  = [ "Head forward" ,  1,     0,   2050,   1230,      1600,     -1,   -1,   -1,    -1 ]
m2  = [ "Neck CW"      ,  2,     0,   3000,   1100,      2045,      1,   -1,   -1,    -1 ]

# The list of all the motors
Motors = [  m1, m2 ]


##----------------------------------Main Function-----------------------------------

##  This is what the Core calls, and loops continuously during robot function
def create_motion( world ):

    while world['power state']:
        
        # tries to connect every 1s
        if world['motion state'] == 'disconnected':
            try:
                time.sleep(1)
                result = init_servos(world['motor port'])
                if result == False:
                    time.sleep(1)
                    print('motor connection Failed')
                if result == True:
                    world['motion state'] = 'connected'
                    print('motor connection Success')
            except Exception as e:
                print('motor failed to connect')
                print(e)


        if world['motion state'] == 'connected':
            
            if world['main state'] == 'sleep':
                relax_all()
                time.sleep(1)
                

            if world['main state'] == 'awake':
                pos1 = m2[5]
                pos2 = pos1 + 100
                move(2, pos1)
                time.sleep(2)
                move(2, pos2)
                time.sleep(2)
                
            
            if world['main state'] == 'sex':
                pos1 = m1[5]
                pos2 = pos1 + 100
                move(1, pos1)
                time.sleep(2)
                move(1, pos2)
                time.sleep(2)
        

        time.sleep(0.2)

    
    relax_all()
    closeport()


##------------------------- Basic Functions -----------------------------------

##### reads the serial ports
def list_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    print('found Serial ports for Motors:')
    print(result)
    return result


### Close port
def closeport():
    portHandler.closePort()


### Initialize servos --------------
def init_servos( port ):
    condition = True

    ## Connects to motors and callibrates them if ok
    if condition == True:
        global packetHandler
        global portHandler
        portHandler = port_handler.PortHandler(port)
        packetHandler = packet_handler.PacketHandler(0)
        condition = False
        if portHandler.openPort():
             print("Succeeded to open the port")
        else:
            print("Failed to open the port")
     
            quit()
        # Set port baudrate
        if portHandler.setBaudRate(BAUDRATE):
            print("Succeeded to change the baudrate")
            condition = True
        else:
            print("Failed to change the baudrate")
            quit()

        relax_all()

        # test the motors to see condition
        errors = 0
        for m in Motors:
            ID = m[1] 
            result = read(ID, curr_pos )
            if result is None:
                errors = errors +1
            result = read(ID, curr_pos )
            if result is None:
                errors = errors +1
        percent = 100* errors /( len(Motors)*2)
        print( ' Percentage of Motor read errors: ' + str(percent))

    return condition


#### ------------------Ping the servo with ID x
# Function returns true if ping or false if no ping

def ping(IDD):
    print("Try to Ping Motor: " + str(IDD) )
    data, com, error = packetHandler.ping(portHandler, IDD)

    if com != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(com))
        return False
    elif error != 0:
        print("%s" % packetHandler.getRxPacketError(error))
        return False
    else:
        print("[ID:%03d] ping Succeeded. SCServo model number : %d" % (IDD, data))
        return True


####------------------- Write to register
# IDD is the servo ID
# reg is the register ( like torque = 40 )
# data is what to write to register
# returns true if sucessful

def write(IDD, reg, data):
    #print('writing motor '+str(IDD)+ ' register ' +str(reg) )
    # finds the motor from global variableF.
    motorr = m1
    for x in Motors:
        if x[1] == IDD:
            motorr = x

    motor_typee = motorr[2]
    #print( "writing to motor " + str(motorr[1]))

    global packID
    if (motor_typee != packID ):   # different packet handler for different motor types
        global packetHandler
        packetHandler = packet_handler.PacketHandler(motor_typee)
        packID = motor_typee
    
    try:
        com, error= packetHandler.write2ByteTxRx(portHandler, IDD, reg, int(data))
        if com != COMM_SUCCESS:
           # print(str(IDD) + ' comm error: ' + str(com)  )
            com, error= packetHandler.write2ByteTxRx(portHandler, IDD, reg, int(data))
            
        if error != 0:
            #print(str(IDD) + ' error code: ' + str(error))
            com, error= packetHandler.write2ByteTxRx(portHandler, IDD, reg, int(data))
            
        else:
            return True
    except Exception as e:
        print('serial write error')
        print(e)
        return False

#### ------------------Read from register
# IDD is the servo ID
# reg is the register ( like torque = 40 )
# returns the data or returns False

def read(IDD, reg):
    motorr = m1
    for x in Motors:
        if x[1] == IDD:
            motorr = x
    motor_typee = motorr[2]
    #print( "reading from motor " + str(motorr[1]))

    global packID
    if (motor_typee != packID ):   # different packet handler for different motor types
        global packetHandler
        packetHandler = packet_handler.PacketHandler(motor_typee)
        packID = motor_typee
    try:
        data, com, error= packetHandler.read2ByteTxRx(portHandler, IDD, reg)
        if com != COMM_SUCCESS:
            #print(str(IDD) + ' comm error: ' + str(com))
            data, com, error= packetHandler.read2ByteTxRx(portHandler, IDD, reg)
            
        elif error != 0:
            #print(str(IDD) + ' error code: ' + str(error))
            data, com, error= packetHandler.read2ByteTxRx(portHandler, IDD, reg)
            
        else:
            if reg == curr_pos:
                if ( motor_typee == 2 ):
                    scs_present_position = SCS_LOWORD(data)
                    scs_present_speed = SCS_HIWORD(data)
                    return scs_present_position
                else:
                    return data
            else:
                return data
    except Exception as e: 
        print('serial read error')
        print(e)
        return False

# moves a motor (desitination in steps)
def move(IDD, val):
    write(IDD, goal_pos, val)



#### Set motor position to middle (only for 360 rotation motors)
# middle position is 2047
def set_mid(IDD):
    result = write(IDD, 40, 128)
    return result

#### Read Position
def read_pos(IDD):
    dat = read(IDD, curr_pos)
    return dat

#### relax all the motors
def relax(motID):
    write(motID, 40, 0)

def relax_all():
    for m in Motors:
        write( m[1] , 40, 0)


if __name__ == "__main__":
    list_ports()