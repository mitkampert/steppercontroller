import socket
import RPi.GPIO as GPIO
import serial
import time

# set serial connection with Arduino, default baud rate = 9600
nano_serial_R = serial.Serial('/dev/ttyUSB0', 9600)
nano_serial_L = serial.Serial('/dev/ttyUSB1', 9600)
# delay set on the Aruduino (us)
DELAY = 1000

DIR_R = 6
DIR_L = 16
ENA = 5
SERVO = 17
ARD_M = 1

DEFAULT = 7.5
current_cam = DEFAULT

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_R, GPIO.OUT)
GPIO.setup(DIR_L, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(SERVO, GPIO.OUT)
GPIO.setup(ARD_M, GPIO.OUT)
cam = GPIO.PWM(SERVO, 50)
cam.start(DEFAULT)

manual = True
GPIO.output(ARD_M, False)

UDP_IP = "0.0.0.0" # listen to everything
UDP_PORT = 12342

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def to_signal(command, reverse):
    if command[0] == 'd':
        steps = int(command[1:])*13
        if (steps > 0 and not reverse) or (steps < 0 and reverse):
            GPIO.output(DIR_R, True)
            GPIO.output(DIR_L, True)
        elif (steps < 0 and not reverse) or (steps > 0 and reverse):
            GPIO.output(DIR_R, False)
            GPIO.output(DIR_L, False)

        nano_serial_R.write(abs(steps))
        nano_serial_L.write(abs(steps))
        
        # wait for motors to finish
        time.sleep(abs((steps*DELAY*2*10**-6) + 1))



    elif command[0] == 't':
        steps = int(command[1:]) * 10
        if (steps > 0 and not reverse) or (steps < 0 and reverse):
            GPIO.output(DIR_R, True)
            GPIO.output(DIR_L, False)
            

        elif (steps < 0 and not reverse) or (steps > 0 and reverse):
            GPIO.output(DIR_R, False)
            GPIO.output(DIR_L, True)

        nano_serial_R.write(abs(steps))
        nano_serial_L.write(abs(steps))

        # wait for motors to finish
        time.sleep(abs((steps*DELAY*2*10**-6) + 1))
            

    elif command[0] == 'c':
        cam.ChangeDutyCycle(int(command[:-1]))
    elif command[0] == 'p':
        pass #run photo script

try:
    while True:
        data, addr = sock.recvfrom(512)
        data = data.decode("utf-8")
        if data[0] == 'c':
            control = data[1:].split(",")

            # arm / disarm handbrake
            if control[4] == "1":
                GPIO.output(ENA, False)
            elif control[4] == "0":
                GPIO.output(ENA, True)

            # camera movement

            # do nothing
            if control[5] == "0":
                pass
            # move up
            elif control[5] == "1":
                if current_cam <= 11.5:
                    cam.ChangeDutyCycle(current_cam + 1)
            # move down
            elif control[5] == "2":
                if current_cam >= 3.5:
                    cam.ChangeDutyCycle(current_cam - 1)
            # reset position
            elif control[5] == "3":
                current_cam = DEFAULT
                cam.ChangeDutyCycle(current_cam)

            # set steering input from gamepad
            if float(control[0]) > 0:
                steer = float(control[0])*-100
            elif float(control[0]) < 0:
                steer = float(control[0])*-100
            else:
                steer = 0

            # set throttle value from gamepad
            if control[3] == "1":
                throttle = float(control[1])*100
            elif control[3] == "0":
                throttle = float(control[2])*-100

            # add or subtract throttle and steering inputs to set correct throttle values for both sides of vehicle
            throttle_r = throttle + steer
            throttle_l = -throttle + steer

            print(throttle_r)

            # set direction based on positive/negative value for both sides 
            if throttle_r >= 0:
                GPIO.output(DIR_R, True)
            elif throttle_r < 0:
                GPIO.output(DIR_R, False)

            if throttle_l >= 0:
                GPIO.output(DIR_L, True)
            elif throttle_l < 0:
                GPIO.output(DIR_L, False)


            # limit value to 100 in case throttle and steering input result in a greater value
            if abs(throttle_r) > 100:
                throttle_r = 100
            if abs(throttle_l) > 100:
                throttle_l = 100
            
            # encode throttle value to ASCII character
            throttle_r = chr(int(abs(throttle_r)*0.93)+33).encode("utf-8")
            throttle_l = chr(int(abs(throttle_l)*0.93)+33).encode("utf-8")

            # Write the ASCII bite to the serial port
            nano_serial_R.write(throttle_r)
            nano_serial_L.write(throttle_l)

        elif data[0] == 'm':
            if data[1] == '0':
                manual = False
                GPIO.output(ARD_M, True)
                

            elif data[1] == '1':
                manual = True
                GPIO.output(ARD_M, False)

            while not manual:
                route = []
                done = []
                data, addr = sock.recvfrom(512)
                data = data.decode("utf-8")
                if data[0] != 'c' and data[0] != 'x':
                    route.append(data)
                while data != 'x':
                    data, addr = sock.recvfrom(512)
                    data = data.decode("utf-8")
                    
                    route.append(data)

                print(route)

                for command in route:
                    to_signal(command, False)

                    if command[0] == 'r':
                        done.reverse()
                        for step in done:
                            if step == 'c' or step == 'p':
                                pass
                            else:
                                to_signal(step, True)
                                print(f"{step} done in reverse")
                        done = []
                    elif command == "m1":
                        manual = True
                        GPIO.output(ARD_M, False)
                    else:
                        print(f"{command} done")
                        done.append(command)
                                     


except KeyboardInterrupt:
    print("cleanup")
    GPIO.cleanup()

