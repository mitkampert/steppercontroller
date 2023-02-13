import socket
import time
import pygame
from colorama import Fore
from datetime import timedelta

pygame.init()
WIDTH = 1920
HEIGHT = 720
scr = pygame.display.set_mode((WIDTH, HEIGHT))
 
# set the pygame window name
pygame.display.set_caption('CMS')

imp = pygame.image.load("client/img/rov.png").convert()
imp = pygame.transform.scale(imp,(468*0.6, 842*0.6))

pp_msg = pygame.image.load("client/img/pp-msg.png").convert_alpha()

font = pygame.font.SysFont("freemono", 30)

forward = 1
hbk = 0
cam_action = 0
manual_mode = True
route = []

joystick = pygame.joystick.Joystick(0)
joystick.init()

# UDP_IP = "172.26.230.50"
UDP_IP = "192.168.191.151"
UDP_PORT = 12342

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def compress(command):
    if command == "return":
        result = 'r'
    elif command == "manual":
        result = 'm1'
    elif command == "photo":
        result = 'p'
    else:
        command = command.split('(')
        if command[0] == "forward":
            result = f"d{command[1][:-1]}"
        elif command[0] == "reverse":
            result = f"d-{command[1][:-1]}"
        elif command[0] == "left":
            result = f"t{command[1][:-1]}"
        elif command[0] == "right":
            result = f"t-{command[1][:-1]}"
        elif command[0] == "cam":
            result = f"c{command[1][:-1]}"

    return result

def generate_window(vl, vr, steer, hbk):
    scr.fill((0,0,0))
    scr.blit(imp, (WIDTH/2 - (468*0.6)/2, 40))

    t = time.time()
    td = timedelta(seconds=int(t-start))
    t_main = font.render("Mission duration:", True, (0, 255, 4))
    t_text = font.render(f"t = +{td}", True, (0, 255, 4))

    vl_main = font.render("Left track:", True, (0, 255, 4))
    vr_main = font.render("Right track:", True, (0, 255, 4))

    if hbk == 1:
        hbk_text = font.render("Handbrake: ON", True, (0, 255, 4))
    elif hbk == 0:
        hbk_text = font.render("Handbrake: OFF", True, (255, 0, 0))
    else:
        hbk_text = font.render("Handbrake: N/A", True, (255, 0, 0))

    if vl != 0:
        vl = (60*10**6)/((50000/(100*vl))*800)
    if abs(vl) < 8:
        vl = 0
    if vl > 150:
        vl = 150
    elif vl < -150:
        vl = -150

    if vr != 0:
        vr = (60*10**6)/((50000/(100*vr))*800)
    if abs(vr) < 8:
        vr = 0
    if vr > 150:
        vr = 150
    elif vr < -150:
        vr = -150

    vl_tacho = font.render(f"{int(vl)} RPM", True, (0, 255, 4))
    vr_tacho = font.render(f"{int(vr)} RPM", True, (0, 255, 4))

    if steer == 0:
        pygame.draw.rect(scr, (0, 255, 4), pygame.Rect(400, 620, 1920-800, 75), 2)
        pygame.draw.rect(scr, (0, 255, 4), pygame.Rect((1920/2)-1, 625, 2, 65))
    elif steer > 0:
        pygame.draw.rect(scr, (0, 255, 4), pygame.Rect(400, 620, 1920-800, 75), 2)
        pygame.draw.rect(scr, (0, 255, 4), pygame.Rect((1920/2)-1, 625, 2+(steer*555), 65))
    elif steer < 0:
        pygame.draw.rect(scr, (0, 255, 4), pygame.Rect(400, 620, 1920-800, 75), 2)
        pygame.draw.rect(scr, (0, 255, 4), pygame.Rect(int((1920/2)-1+(steer*555)), 625, int((-steer*555)+2), 65))

    vlt = vl*1.2
    vrt = vr*1.2

    if vlt <= 0:
        pygame.draw.rect(scr, (0, 255, 4), pygame.Rect(838, 310, 24, 2-vlt))
    elif vlt > 0:
        pygame.draw.rect(scr, (0, 255, 4), pygame.Rect(838, 310-vlt, 24, 2+vlt))
    if vrt <= 0:
        pygame.draw.rect(scr, (0, 255, 4), pygame.Rect(1058, 310, 24, 2-vrt))
    elif vrt > 0:
        pygame.draw.rect(scr, (0, 255, 4), pygame.Rect(1058, 310-vrt, 24, 2+vrt))



    scr.blit(t_main, (10, 10))
    scr.blit(t_text, (10, 40))

    scr.blit(vl_main, (550, 300))
    scr.blit(vr_main, (WIDTH-750, 300))

    scr.blit(vl_tacho, (580, 350))
    scr.blit(vr_tacho, (WIDTH-710, 350))

    scr.blit(hbk_text, (1600, 10))


    if hbk == 2:
        scr.blit(pp_msg, (0, 0))
    
    pygame.display.flip()

pygame.display.flip()

start = time.time()
while True:
    generate_window(0, 0, 0, 2)
    print(f"{Fore.GREEN}Entered manual mode.{Fore.RESET}")
    while manual_mode == True:
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if joystick.get_button(5):
                    hbk = abs(hbk-1)
                elif joystick.get_button(0):
                    sock.sendto(bytes(f"p", encoding='utf-8'), (UDP_IP, UDP_PORT))
                # elif joystick.get_button(1):
                #     print("b")
                # elif joystick.get_button(2):
                #     print("x")
                elif joystick.get_button(3):
                    sock.sendto(bytes(f"m0", encoding='utf-8'), (UDP_IP, UDP_PORT))
                    manual_mode = False
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
        
        sock.sendto(bytes(f"c{x_axis},{throttle},{reverse},{forward},{hbk},{cam_action}", encoding='utf-8'), (UDP_IP, UDP_PORT))

        cam_action = 0

        if forward == 1:
                throttle_cms = throttle
        elif forward == 0:
            throttle_cms = -reverse

        generate_window(throttle_cms + x_axis, throttle_cms - x_axis, x_axis, hbk)
        time.sleep(0.01)
    
    print(f"{Fore.GREEN}Entered pre-programmed route  -  type 'help' to get a list of available commands.{Fore.RESET}\n")
    while manual_mode == False:
        generate_window(0, 0, 0, 2)
        confirmed = False
        while not confirmed:
            command = input("Next step: ").lower()
            while command != "fin":
                if command == "manual":
                    route.append("manual")
                    manual_mode = True
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
cam(x)      -   move camera. 0 = flat, pos = up, neg = down. Range = (3.5 , 11.5)   
photo       -   captures a photo with the camera.  
manual      -   return to manual mode. 

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
                            raw_command = compress(commands)
                        print(f"{Fore.BLUE}Program valid.{Fore.RESET}")
                    except:
                        print(f"{Fore.RED}Program error. Please reset and try again.{Fore.RESET}")
                
                else:
                    route.append(command)
                
                command = input("Next step: ").lower()
        


            command = None
            check = None
            while check != 'y' and check != 'n' and check != '':
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
                raw_command = compress(commands)
                sock.sendto(bytes(raw_command, encoding='utf-8'), (UDP_IP, UDP_PORT))
            sock.sendto(bytes('x', encoding='utf-8'), (UDP_IP, UDP_PORT))
            print(f"{Fore.GREEN}program sent.{Fore.RESET}\n")
            route = []
        except:
            print(f"{Fore.RED}Compilation error. Program has been cleared, please try again.{Fore.RESET}\n")
            route = []