import argparse
import os

import numpy as np
from PIL import Image

import cv2
import imutils
import pytesseract
from imutils import paths

# grab the paths to the input images and initialize our images list
print("[INFO] loading images...")
imagePaths = sorted(list(paths.list_images('captured_images/section')))
images = []

# loop over the image paths, load each one, and add them to our
# images to stich list
for imagePath in imagePaths:
	print (imagePath)
	image = cv2.imread(imagePath)
	images.append(image)

# initialize OpenCV's image sticher object and then perform the image
# stitching
print("[INFO] stitching images...")
stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
(status, stitched) = stitcher.stitch(images)

# if the status is '0', then OpenCV successfully performed image
# stitching
if status == 0:
	# check to see if we supposed to crop out the largest rectangular
	# region from the stitched image
	if 2 > 1:
		# create a 10 pixel border surrounding the stitched image
		print("[INFO] cropping...")
		stitched = cv2.copyMakeBorder(stitched, 10, 10, 10, 10,
			cv2.BORDER_CONSTANT, (0, 0, 0))

		# convert the stitched image to grayscale and threshold it
		# such that all pixels greater than zero are set to 255
		# (foreground) while all others remain 0 (background)
		gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
		thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

		# find all external contours in the threshold image then find
		# the *largest* contour which will be the contour/outline of
		# the stitched image
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		c = max(cnts, key=cv2.contourArea)

		# allocate memory for the mask which will contain the
		# rectangular bounding box of the stitched image region
		mask = np.zeros(thresh.shape, dtype="uint8")
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

		# create two copies of the mask: one to serve as our actual
		# minimum rectangular region and another to serve as a counter
		# for how many pixels need to be removed to form the minimum
		# rectangular region
		minRect = mask.copy()
		sub = mask.copy()

		# keep looping until there are no non-zero pixels left in the
		# subtracted image
		while cv2.countNonZero(sub) > 0:
			# erode the minimum rectangular mask and then subtract
			# the thresholded image from the minimum rectangular mask
			# so we can count if there are any non-zero pixels left
			minRect = cv2.erode(minRect, None)
			sub = cv2.subtract(minRect, thresh)

		# find contours in the minimum rectangular mask and then
		# extract the bounding box (x, y)-coordinates
		cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		c = max(cnts, key=cv2.contourArea)
		(x, y, w, h) = cv2.boundingRect(c)

		# use the bounding box coordinates to extract the our final
		# stitched image
		stitched = stitched[y:y + h, x:x + w]
	
	from datetime import datetime
	now = datetime.now() 
	# write the output stitched image to disk
	output_file = "output" + now.strftime("%m/%d/%Y, %H:%M:%S") +".png" 
	cv2.imwrite(output_file, stitched)
	print("Stiched Image Saved")

	# display the output stitched image to our screen
	#cv2.imshow("Stitched", stitched)
	#cv2.waitKey(200)

# otherwise the stitching failed, likely due to not enough keypoints)
# being detected
else:
	print("[INFO] image stitching failed ({})".format(status))


# # load the example image and convert it to grayscale
# #image = cv2.imread( output_file )
# image = stitched
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# gray = cv2.medianBlur(gray, 3)
# gray = cv2.threshold(gray, 0, 255,
# 		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# #cv2.imshow("Image", gray)

# # write the grayscale image to disk as a temporary file so we can
# # apply OCR to it
# filename = "{}.png".format(os.getpid())
# cv2.imwrite(filename, gray)

# # load the image as a PIL/Pillow image, apply OCR, and then delete
# # the temporary file
# text = pytesseract.image_to_string(Image.open(filename))
# #os.remove(filename)

# #text=text.split(' ',)
# #test=text[19]
# print("Detected text: " + text)
# word = text.split(" ")[19]
# print("Word of Interest : " + word)
# #show the output images
# #cv2.imshow("Image", image)
# #cv2.imshow("Output", gray)
# #cv2.waitKey(5)

# # from PyDictionary import PyDictionary

# # try:
# # 	dictionary=PyDictionary()
# # 	print(dictionary.meaning(word))
# # except:
# # 	print ("")
