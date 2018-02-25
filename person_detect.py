#import the necessary packages
from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

import sys
sys.path.append('pyimagesearch')
from tempimage import TempImage

import face_detect

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def detect(conf, oimage):

	# load the image and resize it to (1) reduce detection time
	# and (2) improve detection accuracy
	image = imutils.resize(oimage, width=min(400, oimage.shape[1]))
	orig = image.copy()

	# detect people in the image
	(rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
		padding=(8, 8), scale=1.05)

	# draw the original bounding boxes
	#for (x, y, w, h) in rects:
	#	cv2.rectangle(orig, (x, y), (x + w, y + h), (255, 0, 0), 2)

	# apply non-maxima suppression to the bounding boxes using a
	# fairly large overlap threshold to try to maintain overlapping
	# boxes that are still people
	rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
	pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

	# draw the final bounding boxes
	for (xA, yA, xB, yB) in pick:
		
		#cv2.rectangle(image, (xA, yA), (xA + xB, yA + yB), (255, 0, 0), 2)
		#t = TempImage('data')	
		#cv2.imwrite(t.path,image)
		
		print("[INFO] done capturing frame...")
		
		sub_face = image[yA:(yA+yB), xA:(xA+xB)]
		face_detect.detectface(conf, oimage)
	
	# show some information on the number of bounding boxes
	#filename = imagePath[imagePath.rfind("/") + 1:]
	#print("[INFO] : {} original boxes, {} after suppression".format(
	#	 len(rects), len(pick)))


