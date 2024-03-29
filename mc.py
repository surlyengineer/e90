#import serial
import pygame
import time

#serialPort = '/dev/tty.usbserial-A7004Jg4' # Arduino Mega
#serialPort = '/dev/tty.usbmodemfd121'       # Arduino Uno
#baudRate = 9600

# Open Serial Connection to Arduino Board
#ser = serial.Serial(serialPort, baudRate, timeout=1);

'''
Gets joystick data and prints it
'''
def hci_init():
    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()
    print('Initialized Joystick : {}'.format(j.get_name()))
    return j

def hci_input(j):
    pygame.event.pump()

    # Used to read input from the two joysticks       
    steering = j.get_axis(0)
    throttle = j.get_axis(3)
    return (steering, throttle)

def main():
    j = hci_init()
    while True:
        print(hci_input(j))
