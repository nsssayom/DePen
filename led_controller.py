from gpiozero import Button, LED
import threading
import time
from signal import pause
from time import sleep
import state

red = LED(0)
green = LED(5)
blue = LED(6)

# TODO: Flash LED

def async_led():
    global red, green, blue
    while True:
        if state is 'init':
            red.on()
            green.off()
            blue.off()
        elif state is 'ready':
            red.on()
            blue.on()
            green.off()
        elif state is 'error_single_tap':
            blue.off()
            green.off()
            
            red.on()
            sleep(.33)
            red.off()
            sleep(.33)

            red.on()
            sleep(.33)
            red.off()
            sleep(.33)

            red.on()
            sleep(.33)
            red.off()
            sleep(.33)
            stste.state = 'ready'
            
        elif state is 'scanning':
            blue.on()
            red.off()
            green.off()
        
        elif state is 'result':
            blue.off()
            red.off()
            green.on()

        elif state is 'no_result':
            blue.off()
            green.off()
            
            red.on()
            sleep(.22)
            red.off()
            sleep(.22)

            red.on()
            sleep(.22)
            red.off()
            sleep(.22)

            red.on()
        
        elif state is 'result_cycle':
            blue.off()
            green.off()
            
            red.on()
            sleep(.22)
            red.off()
            sleep(.22)

            red.on()
            sleep(.22)
            red.off()
            sleep(.22)

            red.on()
            sleep(.22)
            red.off()
            sleep(.22)
            stste.state = 'result'


def start_led():
    t = threading.Thread(target=async_led)
    t.start()
