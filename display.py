import os
import sys
import time
from time import sleep

from PIL import ImageFont

import state
from display_driver import get_device
from luma.core.render import canvas
from luma.core.virtual import terminal
from wordnet import get_synset


def init_terminal():
    try:
        device = get_device()
        device.contrast(255)
        font = make_font('Consolas.ttf', 12)
        term = terminal(device, font)
        return term
    except Exception as e:
        print ("Error Initializing Display Driver : {0}".format(e))

def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)

def print_definition(word, index, new = False):
    term = init_terminal()
    term.clear()
    term.animate = True
    synset = get_synset(word)

    if synset is None:
        text = "No definition found"
        term.puts(text)
        print (text)
        return False

    if index > 4:
        index = index % 5
        if not new:
            if index is 0:
                state.state = 'result_cycle'                    # TODO: Define LED for no_result [Red Blinking]
    if index > len(synset) - 1:
        index = index % len(synset)
        if not new:
            if index is 0:
                state.state = 'result_cycle'                    # TODO: Define LED for no_result [Red Blinking]
    defset = synset[index]
    text = word + " [" + defset['lexname'] + "] " + defset['definition']
    term.puts(text)
    print (text)
    return True

def print_prompt(msg):
    term = init_terminal()
    term.clear()
    term.animate = True
    text = msg
    term.puts(text)
    print (text)

def test():
    term = init_terminal()
    term.animate = True
    term.puts("\n   Marry   \n Christmas ")
    sleep(30)

#test()
