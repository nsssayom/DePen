#!/usr/bin/python

import datetime
import subprocess
import sys
from signal import pause
from time import sleep

from display import print_definition, print_prompt
from gpiozero import Button

was_held = False
definition_index = 0
word = sys.argv[1]      # TODO: Add OpenCV routines here
batch_id = None         # Identify each scan run with timestamp. None if no scan is performed
process = None

def held():
    global process
    global was_held
    global batch_id
    was_held = True
    print("Button HELD")
    batch_id = str(datetime.datetime.now()).replace(" ", "_")
    print ("Starting new Batch: {0}".format(batch_id))
    process = subprocess.Popen(['python3', 'read_text.py', batch_id])

def released():
    global process
    global was_held
    global word
    global batch_id
    if not was_held:
        pressed()
    else:
        print("Button Released from HOLD state")
        process.terminate()

        print_prompt("Searching meaning for \n{0}".format(word))    # TODO: word will be received here 
        print_definition(word, 0)
        
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
        print_prompt ("Please hold the button and scan a word")
    
button = Button(21)
print_prompt ("Welcome to DePen")
#button.wait_for_press()
button.when_held = held
button.when_released = released
pause()
