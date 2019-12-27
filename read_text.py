import datetime
import io
import os
import subprocess
import sys
import threading
import time
from time import sleep

import numpy as np
from PIL import Image

import cv2
import picamera
from display_driver import get_device

# create a pool of image processors
done = False
lock = threading.Lock()
pool = []
batch_id = sys.argv[1]

def trigger_done():
    global done
    done = True

class ImageProcessor(threading.Thread):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.start()

    def run(self):
        # this method runs in a separate thread
        global done
        device = get_device()
        while not self.terminated:
            # wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    self.stream.seek(0)

                    # read the image and display it on screen
                    photo = Image.open(self.stream)
                    device.display(photo.convert(device.mode))
                    opencvImage = cv2.cvtColor(np.array(photo), cv2.COLOR_RGB2BGR)
                    #crop_img = opencvImage[0:64, 20:102]
                    dir_name = os.path.join('captured_images/', batch_id) 
                    
                    if not os.path.exists(dir_name):
                        os.mkdir(dir_name)
                    file_path = str(os.path.join(dir_name, str(datetime.datetime.now()) + ".jpg"))
                    cv2.imwrite( file_path, opencvImage)
                    
                    #photo = Image.fromarray(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
                    # set done to True if you want the script to terminate
                    # at some point
                    # done=True
                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()

                    # return ourselves to the pool
                    with lock:
                        pool.append(self)

def streams():
    while not done:
        with lock:
            if pool:
                processor = pool.pop()
            else:
                processor = None
        if processor:
            yield processor.stream
            processor.event.set()
        else:
            # when the pool is starved, wait a while for it to refill
            time.sleep(0.1)

with picamera.PiCamera() as camera:
    pool = [ImageProcessor() for i in range(4)]

    # set camera resolution
    camera.resolution = (640, 480)
    camera.framerate = 3

    print("Starting camera preview...")
    camera.start_preview()
    time.sleep(2)

    print("Capturing video...")
    try:
        device = get_device()
        camera.capture_sequence(streams(), use_video_port=True, resize=device.size)

        # shut down the processors in an orderly fashion
        while pool:
            with lock:
                processor = pool.pop()
            processor.terminated = True
            processor.join()
    except KeyboardInterrupt:
        pass
