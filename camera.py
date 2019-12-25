from picamera import PiCamera
from time import sleep

camera = PiCamera()

def capture(batch_id):
    global camera    
    camera.capture('captured_images/' + batch_id +'/image.jpg')
    camera.stop_preview()