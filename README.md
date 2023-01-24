# Stepper motor controller

## Control stepper motors using an Xbox One gamepad

Run client.py on your pc with the xbox controller connected via USB. This program will read the controller inputs and send these to connected server.

Run server.py on a Raspberry Pi. Make sure it is connected to the internet and the same network as your client pc. Once the server and client script are running
and connected to eachother, the server program will receive the controller inputs from the client, and convert these to instructions for the Arduino. 
Direction and handbrake are controlled using digital signals from the GPIO. Throttle and steering inputs are combined to reach the final motor speed ranging from 0 to 100.
This value is then converted to ASCII ranging from 0 to 93. For each loop this ASCII byte is sent to the Arduino over the serial connection. 

The main.ino file is stored on the Arduino and converts the input signals from the Raspberry Pi to digital signals for the stepper motor driver. A pulse signal to move the motor 1 step, the delay between steps is based on the throttle value received over the serial connection. The direction is based on the value of the digital input pin connected to the Raspberry Pi GPIO and the handbrake (enable pin) is also connected to the Raspberry Pi GPIO. 

The GPIO pins for both the Raspberry Pi and Arduino can be changed to other pins if you would like to use different pins. The default pins used in this repository are:

Raspberry Pi:
    - 5 (ENA)
    - 6 (DIR) to Arduino controlling right hand side.
    - 16 (DIR) to Arduino controlling left hand side.

Arduino:
    - D2 (Input pin receiving forward/reverse value from Raspberry Pi)
    - D3 (Input pin receiving enable value from Raspberry Pi)
    - D9 (Output pin setting the direction value of the stepper driver)
    - D10 (Output pin sending a pulse signal to the stepper driver)
    - D11 (Output pin enabling or disabling the stepper driver)