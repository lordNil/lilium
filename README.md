# lilium
Code for Robotic Brain V1

The Code here will be the open source version of the brain for lilium robotics. It is intended to be a template code with various functions and parameters that people can play and explore with. That way, the brain can be improved as new external modules are added. The production code is a customized implementation of this open source version. 

The Architecture of the code:

- The main file is Core.py  :   This is a small script that starts all the other code using python multi-processing to use multiple cpu-cores. It also shares data between processes using a dict object called 'world'. Each of the processes that are started have their own python file, and are called: Motion.py, Vision.py, UI.py, Sound.py, and  Neural.py. 

- Motion.py and the Motion folder :   This file handles robotic motion and includes things like data on each of the motors, read/write/record functions on the motors. The motion folder contains other files that are used by Motion.py such as recordings of animations. 

- Vision.py and the Vision folder :  This file handles robotic vision and includes things like streaming from cameras, image processing, and also different object detection algorithms. The vision folder contains data that Vision.py uses such as neural network models. 

- Sound.py and the Sound folder  :  This file handles robotic sound, and includes things like working with speakers/microphones, playing/adjusting sound, text-to-speach, speach-to-text, and different chatbots. The sound folder contains data that Sound.py uses such as voice lines, audiobooks, and chatbot data. 

- UI.py and the UI folder  :  This file handles robotic UI options, and includes a few different UI's such as a bluetooth serial connection, a GUI, and a web app. 

- Neural.py and the Neural folder  :   This python file is empty for now. The plan is to implement a neural network + logic engine to make decisions with the data that is acquired. 
