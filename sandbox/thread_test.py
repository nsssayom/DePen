from gpiozero import Button, LED
import threading
import time
from signal import pause
import random
from time import sleep

button = Button(21)
red = LED(0)
green = LED(5)
blue = LED(6)
state = 0

def thread_function():
    global state, red, green, blue
    while True:
        if state is 0:
            red.on()
            green.off()
            blue.off()
        elif state is 1:
            red.off()
            green.on()
            blue.off()
        else:
            red.off()
            green.off()
            blue.on()


t = threading.Thread(target=thread_function)
t.start()
while True:
    state = random.choice([0,1,2])
    print (state)
    sleep(1)