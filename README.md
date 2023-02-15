# Stepper motor control software for Themaproject ROV mission

## Control stepper motors using an Xbox One gamepad and pre-programmed mode

### client.py
client.py will be running on the controlling pc, an xbox controller must be connected via USB. The software will launch a GUI on which the current controller inputs, 
motor speed, mission duration and handbrake status can be seen. 

#### Controller button functions
- The right and left throttles control forward and reverse speed respectively. 
- The left joystick controls steering input.
- the D-pad controls the camera angle. Up/down move camera up and down, right resets the camera to horizontal position.
- RT enables/disables the handbrake. The handbrake is turned off by default.
- A captures an image using the onboard camera.
- Y sets ROV in pre-programmed mode.

Pre-programmed mode is used for autonomous mode. The user can develop a list of commands to be executed by the ROV. The available commands can be shown by typing "help" when in pre-programmed mode. This will return the following list of available commands:

#### Control commands:
forward(x)  -   move x cm forward.
reverse(x)  -   move x cm backwards.
left(x)     -   move x degrees to the left.
right(x)    -   move x degrees to the right.
return      -   return to original position.
cam(x)      -   move camera. 0 = flat, pos = up, neg = down. Range = (3.5 , 11.5)   
photo       -   captures a photo with the camera.  
manual      -   return to manual mode. 

#### Other commands:
fin     -   finish command sequence.
help    -   this screen right here.
clear   -   clears current commands.
show    -   show current program.
check   -   check if current program is valid

All control data is being sent to the on-board Raspberry Pi which will decode the data further.

### server.py

Run server.py on a Raspberry Pi. Make sure it is connected to the internet and the same network as your client pc. Once the server and client script are running
and connected to eachother, the server program will receive the controller inputs from the client, and convert these to instructions for the Arduino. 
Direction and handbrake are controlled using digital signals from the GPIO. Throttle and steering inputs are combined to reach the final motor speed ranging from 0 to 100.
This value is then converted to ASCII ranging from 0 to 93. For each loop this ASCII byte is sent to the Arduino over the serial connection. 

### Arduino

The main.ino file is stored on the Arduino and converts the input signals from the Raspberry Pi to digital signals for the stepper motor driver. A pulse signal to move the motor 1 step, the delay between steps is based on the throttle value received over the serial connection. The direction is based on the value of the digital input pin connected to the Raspberry Pi GPIO and the handbrake (enable pin) is also connected to the Raspberry Pi GPIO. 

### GPIO

The GPIO pins for both the Raspberry Pi and Arduino can be changed to other pins if you would like to use different pins. The default pins used in this repository are:

#### Raspberry Pi:
- 1 (ARD_M) Communicates with Arduino if manual mode is enabled or not.
- 5 (ENA) Communicates with Arduino if handbrake is enabled or not.
- 6 (DIR_R) to Arduino controlling right hand side.
- 16 (DIR_L) to Arduino controlling left hand side.
- 17 (SERVO) PWM output to control the camera servo.

#### Arduino:

- D2 (Input pin receiving forward/reverse value from Raspberry Pi)
- D3 (Input pin receiving handbrake value from Raspberry Pi)
- D4 (Input pin receiving manual value from Raspberry Pi)
- D9 (Output pin setting the direction value of the stepper driver)
- D10 (Output pin sending a pulse signal to the stepper driver)
- D11 (Output pin enabling or disabling the stepper driver)