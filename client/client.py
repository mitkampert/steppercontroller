import socket
import time
import pygame
from colorama import Fore

pygame.init()

forward = 1
hbk = 0
cam_action = 0
manual_mode = True
mode = 1
route = []

joystick = pygame.joystick.Joystick(0)
joystick.init()

UDP_IP = "192.168.191.151"
UDP_PORT = 12342

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def decode(command):
    if command == "return":
        result = 'r'
    elif command == "manual":
        result = 'm'
    else:
        command = command.split('(')
        if command[0] == "forward":
            result = f"f{command[1][:-1]}"
        elif command[0] == "reverse":
            result = f"r{command[1][:-1]}"
        elif command[0] == "left":
            result = f"t{command[1][:-1]}"
        elif command[0] == "right":
            result = f"t-{command[1][:-1]}"

    return result


while True:
    mode = 1
    print(f"{Fore.GREEN}Entered manual mode.{Fore.RESET}")
    while manual_mode == True:
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
                elif joystick.get_button(3):
                    manual_mode = False
                    mode = 0
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
        
        sock.sendto(bytes(f"{x_axis},{throttle},{reverse},{forward},{hbk},{cam_action},{mode}", encoding='utf-8'), (UDP_IP, UDP_PORT))

        cam_action = 0
        time.sleep(0.01)
    
    print(f"{Fore.GREEN}Entered pre-programmed route  -  type 'help' to get a list of available commands.{Fore.RESET}\n")
    while manual_mode == False:
        confirmed = False
        while not confirmed:
            command = input("Next step: ").lower()
            while command != "fin":
                if command == "manual":
                    manual_mode = True
                    confirmed = True
                    route.append("manual")
                    break
                elif command == "clear":
                    print(f"\n{Fore.BLUE}list cleared{Fore.RESET}\n")
                    route = []
                elif command == 'help':
                    print(f'''Pre-programmed mode commands:
                    
{Fore.RED}Control commands:{Fore.RESET}
forward(x)  -   move x cm forward.
reverse(x)  -   move x cm backwards.
left(x)     -   move x degrees to the left.
right(x)    -   move x degrees to the right.
return      -   return to original position.      

{Fore.RED}Other commands:{Fore.RESET}
fin     -   finish command sequence.
help    -   this screen right here.
clear   -   clears current commands.
show    -   show current program.
check   -   check if current program is valid.\n''')
                elif command == 'show':
                    print(f"\n{Fore.LIGHTBLUE_EX}{route}{Fore.RESET}\n")
                elif command == 'check':
                    try:
                        for commands in route:
                            raw_command = decode(commands)
                        print(f"{Fore.BLUE}Program valid.{Fore.RESET}")
                    except:
                        print(f"{Fore.RED}Program error. Please reset and try again.{Fore.RESET}")
                
                else:
                    route.append(command)
                
                command = input("Next step: ").lower()
        


            command = None
            check = None
            while check != 'y' and check != 'n' and check != '' and not manual_mode:
                print(f"\n{Fore.BLUE}Current program:{Fore.RESET}")
                for commands in route:
                    print(commands)
                check = input("\nConfirm route? (y/N) ").lower()
                if check == 'y':
                    confirmed = True
                elif check == 'n' or check =='':
                    confirmed = False

        try:
            for commands in route:
                raw_command = decode(commands)
                sock.sendto(bytes(raw_command, encoding='utf-8'), (UDP_IP, UDP_PORT))
            sock.sendto(bytes('x', encoding='utf-8'), (UDP_IP, UDP_PORT))
            print(f"{Fore.GREEN}program sent.{Fore.RESET}\n")
            route = []
        except:
            print(f"{Fore.RED}Compilation error. Program has been cleared, please try again.{Fore.RESET}\n")
            route = []