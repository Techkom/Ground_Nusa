# import for PiCamera to OpenCV
from picamera.array import PiRGBArray
from picamera import PiCamera

# import for Motion Detection
from imutils.video import VideoStream
import argparse
import datetime

# General Import
import time
import cv2

class Main:
    def __init__(self, rawCapture,args_video):
        #initialize the camera and grab a reference to the raw capture
        camera = PiCamera()
        camera.resolution = (640,480)
        camera.framerate = 32
        self.rawCapture = PiRGBArray(camera, size=(640,480))
        
        #construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-v","--video", help="path to video file")
        ap.add_argument("-a","--min-area", type=int, default=500, help="minimum area size")
        self.args_video = vars(ap.parse_args())
        
    def Program():
        #if the video argument is None, then we are rading from webcam
        if self.args_video.get("video", None) is None:
            # vs = VideoStream(src=0).start()
            time.sleep(2.0)
            #caputre frames from the camera
            for frame in camera.capture_continous(rawCapture, forman="bgr", use_video_port=True):
                    # grab the raw NumPy array representing the image, the initialize timestamp and occupied/unoccupied text
                    image = frame.array
                    
                    # show the frame
                    cv2.imshow("Frame_1",image)
                    
                    # clear the stream in preparation for the next frame
                    self.rawCapture.truncate(0)
            vs = frame
                
        #otherwise, we are reading from a video file
        else:
            vs = cv2.VideoCapture(self.args_video["video"])
        
        Frame_2 = None
        
        # loop over the frames of the video
        while True:
            #grab the current frame and initialize the occupied/unoccupied text
            frame_text = vs.read()
            frame_text = frame if self.args_video.get("video",None) is None else frame[1]
            text = "Unoccupied"
            
            #if the frame could not be grabbed, then we have reached the end of the video
            if frame_text is None:
                break
            
            #resize the frame, conver it to grayscale, and blur it
            frame = imutils.resize(frame_text, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21,21),0)
            
            #if the first frame is None, initialize it
            if Frame_2 is None:
                Frame_2 = gray
                continue
            
            #compute the absolute difference between the current frame and first frame
            frameDelta = cv2.absdiff(Frame_2, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
            
            #dilate the thresholded image to fill in holes, then find contours on thresholded image
            thresh = cv2.dilate(thresh, None, iterations=2)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            
            #loop over the contours
            for c in cnts:
                #if the contour is too small, ignore it
                if cv2.contourArea(c) < self.args_video["min_area"]:
                    continue
                
                #compute the bounding box for the contour, draw it on the frame, and update the text
                (x,y,w,h) = cv2.boundingRect(c)
                cv2.rectangle(Frame_2,(x,y),(x+w,y+h),(0,255,0),2)
                text = "Occupied"
                
            #draw the text and timestamp on the frame
            cv2.putText(Frame_2,"Room Status: {}".format(text),(10,20),cv2.FONT_HERSHEY_SIMPLEX,0,5,(0,0,255),2)
            cv2.putText(Frame_2,datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10,Frame_2.shape[0]-10),cv2.FONT_HERSHEY_SIMPLEX,0.35,(0,0,255),1)
            
            #show the frame and record if the user presses a key
            cv2.imshow("Frame 2", Frame_2)
            cv2.imshow("Thresh", thresh)
            cv2.imshow("Frame Delta", frameDelta)
            key = cv2.waitKey(1) & 0xFF
            
            #if the 'q' key is pressed, break from the lop
            if key == ord("q"):
                break
        
        #cleanup the camera and close any open windows
        vs.stop() if self.args_video.get("video", None) is None else vs.release()
        cv2.destroyAllWindows

d = Main.Program()
