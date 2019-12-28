#!/usr/bin/python3

import datetime
import subprocess
import sys
from signal import pause
from time import sleep

import state
from display import print_definition, print_prompt
from gpiozero import LED, Button
from image_stiching import get_stitched_image
from ocr import ocr
from wordnet import check_spelling, get_synset
from led_controller import start_led

was_held = False
definition_index = 0
word = None
batch_id = None         # Identify each scan run with timestamp. None if no scan is performed
process = None

def held():
    global process
    global was_held
    global batch_id
    was_held = True
    print("Button HELD")
    batch_id = str(datetime.datetime.now()).replace(" ", "_")
    print ("Starting new Scan Batch: {0}".format(batch_id))
    state.state = 'scanning'                                        # TODO: Define LED for scanning [steady blue]
    process = subprocess.Popen(['python3', 'capture_text.py', batch_id])

def released():
    global process
    global was_held
    global word
    global batch_id
    if not was_held:
        pressed()
    else:
        state.state = 'searching'                                     # TODO: Define LED for searching [blinking blue]
        print("Button Released from HOLD state")
        process.terminate()
        get_stitched_image (batch_id)
        scanned_word = ocr(batch_id)
        word = check_spelling (scanned_word)
        if not word:
            state.state = 'no_result'
            print_prompt("Error in scanning")
            return
        print_prompt("Searching meaning for \n{0}".format(word)) 
        if print_definition(word, 0, True):
            state.state = 'result'                          # TODO: Define LED for no_result [Steady Green]
        else:
            state.state = 'no_result'                       # TODO: Define LED for no_result [Red Blinking]
        
    was_held = False

def pressed():
    global batch_id
    global definition_index
    global word
    print("Button Released from PRESS state")
    if batch_id:
        definition_index = (definition_index + 1)
        print_definition(word, definition_index)
    else:
        state.state = 'error_single_tap'               # TODO: Define LED for error single tap [Blink Red 2 sec]
        print_prompt ("Please hold the button and scan a word")
    
button = Button(21)
state.state = 'init'                                   # TODO: Define LED for init state [steady red]
start_led()
print_prompt ("Welcome to DePen\nPlease Wait...")
print ("State: ", state.state)
get_synset("Welcome")
state.state = 'ready'                                   # TODO: Define LED for ready state  [steady cyan = R + B]
print ("State: ", state.state)
button.when_held = held
button.when_released = released
pause()
