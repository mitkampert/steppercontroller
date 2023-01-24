import socket
import RPi.GPIO as GPIO
import serial

nano_serial_R = serial.Serial('/dev/ttyUSB0', 9600)
nano_serial_L = serial.Serial('/dev/ttyUSB1', 9600)


DIR_R = 6
DIR_L = 16
ENA = 5


GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_R, GPIO.OUT)
GPIO.setup(DIR_L), GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

UDP_IP = "0.0.0.0" # listen to everything
UDP_PORT = 12342 # port

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))



try:
    while True:
        data, addr = sock.recvfrom(512) # random buffer size, doesn't matter here..
        control = data.decode("utf-8").split(", ")

        if control[4] == "1":
            GPIO.output(ENA, False)
        elif control[4] == "0":
            GPIO.output(ENA, True)


        if float(control[0]) > 0:
            steer = float(control[0])*-100
        elif float(control[0]) < 0:
            steer = float(control[0])*-100
        else:
            steer = 0


        if control[3] == "1":
            throttle = float(control[1])*100
        elif control[3] == "0":
            throttle = float(control[2])*-100

        throttle_r = throttle + steer
        throttle_l = throttle - steer

        print(throttle_r)

        if throttle_r >= 0:
            GPIO.output(DIR_R, True)
        elif throttle_r < 0:
            GPIO.output(DIR_R, False)

        if throttle_l >= 0:
            GPIO.output(DIR_L, True)
        elif throttle_l < 0:
            GPIO.output(DIR_L, False)


        if abs(throttle_r) > 100:
            throttle_r = 100
        if abs(throttle_l) > 100:
            throttle_l = 100
        
        throttle_r = chr(int(abs(throttle_r)*0.93)+33).encode("utf-8")
        throttle_l = chr(int(abs(throttle_l)*0.93)+33).encode("utf-8")
        
        nano_serial_R.write(throttle_r)
        nano_serial_L.write(throttle_l)

except KeyboardInterrupt:
    print("cleanup")
    GPIO.cleanup()

