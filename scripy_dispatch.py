import subprocess
from time import sleep

process = subprocess.Popen(['python3', 'picamera_video.py'])
sleep(5)
process.terminate()