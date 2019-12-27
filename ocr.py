import pytesseract
import cv2
from PIL import Image
import os

def ocr(batch_id):
    
    dir_name = os.path.join('processed_images/', batch_id) 

    image = None

    if os.path.exists(dir_name):
        file_path = str(os.path.join(dir_name, "stitched_image.jpg"))
        image = cv2.imread( file_path)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    text = pytesseract.image_to_string(Image.fromarray(gray))

    return text

#print (ocr("section"))