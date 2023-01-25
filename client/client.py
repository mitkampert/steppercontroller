import socket
import time
import pygame
pygame.init()

forward = 1
hbk = 1
cam_action = 0

joystick = pygame.joystick.Joystick(0)
joystick.init()

UDP_IP = "192.168.191.151"
UDP_PORT = 12342

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if joystick.get_button(5):
                hbk = abs(hbk-1)
            # elif joystick.get_button(0):
            #     print("a")
            # elif joystick.get_button(1):
            #     print("b")
            # elif joystick.get_button(2):
            #     print("x")
            # elif joystick.get_button(3):
            #     print("y")
            # elif joystick.get_button(4):
            #     print("lb")
            
        if event.type == pygame.JOYHATMOTION:
            if joystick.get_hat(0) == (0, 1):
                cam_action = 1
            elif joystick.get_hat(0) == (0, -1):
                cam_action = 2
            elif joystick.get_hat(0) == (1, 0):
                cam_action = 3

    x_axis = round(joystick.get_axis(0), 2)
    if abs(x_axis) < 0.1:
        x_axis = 0.0

    throttle = round((joystick.get_axis(5) + 1)/2, 2)
    reverse = round((joystick.get_axis(4) + 1)/2, 2)

    if forward == 1 and throttle == 0 and reverse != 0:
        forward = 0
    elif forward == False and throttle != 0 and reverse == 0:
        forward = 1

    if forward == 1:
        reverse = 0
    elif forward == 0:
        throttle = 0
    
    sock.sendto(bytes(f"{x_axis},{throttle},{reverse},{forward},{hbk},{cam_action}", encoding='utf-8'), (UDP_IP, UDP_PORT))

    cam_action = 0
    time.sleep(0.01)