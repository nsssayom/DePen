import pytesseract
import cv2
from PIL import Image

image = image = cv2.imread("result.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray, 3)
gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

text = pytesseract.image_to_string(Image.fromarray(gray))

print("Detected text: " + text)