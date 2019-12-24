#!/usr/bin/python

import sys
from signal import pause
from time import sleep

from display import print_definition, print_prompt
from gpiozero import Button

was_held = False
is_active = False
definition_index = 0
word = sys.argv[1]

def held():
    global was_held
    was_held = True

def released():
    global was_held
    global word
    global is_active
    global is_new_word
    if not was_held:
        pressed()
    else:
        print("button was held")
        print_prompt("Searching meaning for \n{0}".format(word))
        print_definition(word, 0)
        is_active = True
    was_held = False

def pressed():
    global is_active
    global definition_index
    global word
    print("button was pressed")
    if is_active:
        definition_index = (definition_index + 1) % 5 
        print_definition(word, definition_index)
    else:
        print_prompt ("Please hold the button and scan a word")
    
button = Button(21)
print_prompt ("Welcome to DePen")
#button.wait_for_press()
button.when_held = held
button.when_released = released
pause()