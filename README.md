# Depen
DePen is an optical text scanner device that uses simple camera technology and an custom developed Optical Character Reader (OCR) software to display word definations from hard copy documents. Text inputs are read using a camera module with aid of a plano-convex macro lens. Raspberry Pi (tested with both *Raspberry Pi 4 Model B* and *Raspberry Pi Zero W*) is used as  computational device. Continuous brust shots are taken and stitched to create panaromic image of a word. OpenCV library is used for image processing tasks. Tesseract OCR library is then used to read characters from the image. Finally word definations are displyed in an OLED display which is fetched from WordNet. 

## Implementation

![enter image description here](https://i.imgur.com/jtngLl3.jpg)
