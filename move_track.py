# Importing our modules, download the opencv module from the github distro at: https://github.com/opencv/opencv/tree/4.8.0
# If you don't have the RPi.GPIO module you can install it in your terminal with: pip3 install RPi.GPIO
# If you don't have serial you can also install it in your terminal using: pip3 install pyserial

import cv2
import RPi.GPIO as GPIO
from time import sleep
import serial


# port that we want to use to connect to our arduino, in this case it's /dev/ttyUSB0, 
# To double check that it is our port just run /dev/ttyUSB0 in terminal and if true, it shows up,
# else, it will not.any(iterable)
global port
port = serial.Serial('/dev/ttyUSB0', 9600)


#  Detects moving objects using frame history and sensitivity(varThreshold) The higher the history, the more
# it can learn and apply, the higher the varThreshold, the lower the sensitivvity.
bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=10)

# uses our USB camera(you can use picamera with this setup!)
cam = cv2.VideoCapture(0)

# setting the resolution for smoother performance.
cam.set(3, 160) # set horiz resolution
cam.set(4, 120) # set vert res

# try loop containing all of the detection, it is important that this is a for loop.
try:

   while True:

    # reading our camera stream and making sure that it is "true" with ret
    ret, video_stream = cam.read()

    
    # 120 by 160 
    height, width, _ = video_stream.shape
    #face_cascade = cv2.CascadeClassifier('./opencv/data/haarcascades/haarcascade_frontalface_default.xml')

    #print(f'video frame shape: {video_stream.shape}')    

    # this apples the motion detection from earlier onto our video stream, fg stands for fore ground
    fg = bg_subtractor.apply(video_stream)

    # finds our contours of our detections and assigns them with the variable "contour",  the 
    # "hierarchy" variable tells us things about the contours themselves and is not used in this script.
    contours, hierarchy = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #print(f"contour {contours}", f"hierarchy {hierarchy}")

    # x,y,w,h values from below get put into this list for use later
    boundrect_values_list = []
   
    biggest_area = 0

    biggest_index = 0

    ind = 0

    # creates a new variable cnt
    for cnt in contours:
        
        area = cv2.contourArea(cnt)
        # print(f"area: {area}")
        
        # if area is great than 1050 pixels and less than 10000
        if 1050 < area < 10000:


            # returns the x,y,w,h
            x,y,w,h = cv2.boundingRect(cnt)

            A = str(x) + '\n'
            #print(f" A : {A}")

            port.write(A.encode())
            
            #cv2.rectangle(fg, (x,y),(x+w, y+h), (255,255,255),3)

            print(f"x,y,w,h: {x,y,w,h}")

            

            #print(f"area of bounding rectangle: {area_of_boundrect} ")

            # adds all of the x,y,w,h values from the bounding rectangle above to the boundrect_values_list
            # And puts them in brackets so that they are in one "slot" of the list like this: ([x,y,w,h], other values)
            boundrect_values_list.append([x,y,w,h])
            
            # gets the area of our rectangle by multiplying width and height
            area_of_boundrect = (w * h)


            # if area of our bounding rectangle is greater than our biggest_area variable, which is zero,
            # then we make biggest_area equal to the area of our bounding recatangle and we make
            # biggest_index = to ind.
            if area_of_boundrect > biggest_area:

                    biggest_area = area_of_boundrect

                    biggest_index = ind

            ind = ind + 1
        
            
            # if the length of our list is greater than zero
            # then x,y,w,h = our list's biggest index
            # then we draw rectangles around those with two different image shows "fg" for fore ground 
            # and "video_stream" for regular color instead of white and black.        
            if(len(boundrect_values_list) > 0):

                x,y,w,h = boundrect_values_list[biggest_index]

                cv2.rectangle(fg, (x,y),(x+w, y+h), (200,135,255),3)

                cv2.rectangle(video_stream, (x,y),(x+w, y+h), (200,135,255),3)   

    # showing our fore ground which should be black and white
    cv2.imshow('foreground', fg)

    # showing our regular video stream which will have color
    cv2.imshow('video', video_stream)
    
    # IMPORTANT! Do NOT leave cv2.waitkey(2) empty like this: cv2.waitkey(), it will break the script
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break

# This is why the try loop is important, since it's a try loop, it will only break when we stop the 
# script. Thus, all of this code below runs last.
finally:
    # Destroys  all of our video windows so they don't pile up
    cv2.destroyAllWindows()
    # closes the camera
    cam.release()
    # closes the port to the arduino
    port.close()

                

   



   