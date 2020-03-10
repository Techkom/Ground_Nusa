# import the necessary packages
# library for Image Processing
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

# library for MySQL
import mysql_all as mysql

# library for RPi.GPIO and config
# import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BCM) # GPIO Number


# Variable 
# For Relay
# RELAY_1_GPIO = 17 #GPIO 17
# RELAY_2 GPIO = 27 #GPIO 27
# GPIO.setup(RELAY_1_GPIO, GPIO.OUTPUT) # Assign GPIO Mode
# GPIO.setup(RELAY_2_GPIO, GPIO.OUTPUT) # Assign GPIO Mode
# RELAY_1_ON 	= GPIO.output(RELAY_1_GPIO, GPIO.LOW)
# RELAY_1_OFF = GPIO.output(RELAY_1_GPIO, GPIO.HIGH)
# RELAY_2_ON	= GPIO.output(RELAY_2_GPIO, GPIO.LOW)
# RELAY_2_OFF	= GPIO.output(RELAY_2_GPIO, GPIO.HIGH)

# adelay = 0
# timedelay = 100

# Temp Value for Compare
Temp_Value = 0

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=200, help="minimum area size")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	vs = VideoStream(src=0).start()
	time.sleep(2.0)

# otherwise, we are reading from a video file
else:
	vs = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	frame = vs.read()
	frame = frame if args.get("video", None) is None else frame[1]
	text = 0

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if frame is None:
		break

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue

	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 1, 255, cv2.THRESH_BINARY)[1]
	# th2 = cv2.adaptiveThreshold(frameDelta,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,17,2)
	# th3 = cv2.adaptiveThreshold(frameDelta,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,17,2)

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, None,iterations=8)
	thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, None,iterations=8)
	thresh = cv2.dilate(thresh, None, iterations=1)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	# cnts = cnts[0] if len(cnts) == 2 else cnts[1]

	# loop over the contours
	for c in cnts:
		# print("cnts")
		# print(cnts)
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"]:
			# print(cv2.contourArea(c))
			continue

		# print(cv2.contourArea(c))
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		# (x,y,w,h) = cv2.rectangle(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
		text = len(cnts)

	# draw the text and timestamp on the frame
	cv2.putText(frame, "Mouse: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

	# Print Time
	# print(time.strftime("%c"))

	# show the frame and record if the user presses a key
	cv2.imshow("Feed", frame)
	cv2.imshow("Thresh Just Binary", thresh)
	# cv2.imshow("Thresh Adaptive Mean", th2)	
	# cv2.imshow("Thresh Adaptive Gausian", th3)	
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF

	# Delay
	# time.sleep(0.5)
	time.sleep(0.1)

	# SQL Section
	Value = text
	if (Value != Temp_Value):
		# mysql.mysql_Program(Value)
		Temp_Value = Value
		# RELAY_1_ON
		# RELAY_2_ON
	elif ((Value == Temp_Value) or (Value == 0)):
		# RELAY_1_OFF
		# RELAY_2_OFF
		pass

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()
