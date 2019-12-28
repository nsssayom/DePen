from gpiozero import Button, LED
import threading
import time
from signal import pause
from time import sleep
import state

red = LED(0)
green = LED(5)
blue = LED(6)
flash = LED(17)

# TODO: Flash LED

def async_led():
    global red, green, blue, flash
    while True:
        if state.state is 'init':
            red.on()
            green.off()
            blue.off()
            flash.off()
        elif state.state is 'ready':
            red.off()
            blue.on()
            green.on()
            flash.off()
        elif state.state is 'error_single_tap':
            blue.off()
            green.off()
            flash.off()
            
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
            state.state = 'ready'
            
        elif state.state is 'scanning':
            flash.on()
            sleep(1.5)
            blue.on()
            red.off()
            green.off()
        
        elif state.state is 'result':
            flash.off()
            blue.off()
            red.off()
            green.on()

        elif state.state is 'no_result':
            flash.off()
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
        
        elif state.state is 'result_cycle':
            flash.off()
            blue.off()
            green.off()
            
            green.on()
            sleep(.22)
            green.off()
            sleep(.22)

            green.on()
            sleep(.22)
            green.off()
            sleep(.22)

            green.on()
            sleep(.22)
            green.off()
            sleep(.22)
            state.state = 'result'


def start_led():
    t = threading.Thread(target=async_led)
    t.start()

#ERROR SOLVED? YES