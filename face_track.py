# importing opencv
import cv2
from subprocess import Popen
from time import sleep
import RPi.GPIO as GPIO
from time import sleep
# GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

p = GPIO.PWM(11, 50)



p.start(0)
# getting our camera
cam = cv2.VideoCapture(0)



# using this to recognize a face as a face
face_cascade = cv2.CascadeClassifier('./opencv/data/haarcascades/haarcascade_frontalface_default.xml')

# pop up window is named "preview"
window_name = 'preview'

# naming our window
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)


# this is our callback function from 'detect_image = detect_face(image)' And as you can see our parameter
# is not the same, don't worry this will work it is still passing the cam.read image, this is just 
# where the magic happens!
def detect_face(img):
    
    # detects objects(faces) in image and giving coords to put a white rectangle around the face or object
    coord = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=24, minSize=(40,40))


    # x, y , w , h stand for the x-axis, y-axis, width, and height of our face in our image.
    for (x,y,w,h) in coord:

        # creates rectangle around face
        # the (255,255,255) is color, the (x,y) is our vertex of our rectangle,
        # the (x+y,y+h) is opposite to our vertex which allows for the rectangle to exist,
        # and the 5 at the end is the thickness of our rectangle lines.
        cv2.rectangle(img,(x,y),(x+w,y+h), (255,255,255), 5)
        
        
        
        # gets the center of the detected face
        # x axis plus width divided by 2 and y axis plus height divided by 2
        # gets the center of our deteccted face

        global center
        center = (x + w // 2, y + h // 2)

        # creates circle in the center of the detected face
        cv2.circle(img, center, 5, (255, 255, 0), 2)

        # this variable "label" needs to be a string for cv2.putText, so we use an f string to pass 
        # the "center" variable which is explained above, then we put that in cv2.putText.
        label = f'{center}'
        
        cv2.putText(img, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        # gets the center of our face.
        
        global x_center
        x_center = (x + w // 2)

        global angle
        angle = (x_center / image.shape[1]) * 180

        print(f"image shape: {image.shape[1]}")

        move_servo(round(angle, 1))
    return img

    


while True:

    
    def move_servo(angle):
        


        global duty
        duty = round(-1 * (angle / 18)+ 12,1)

        print(f"duty: {duty}, angle: {round(angle, 1)}, cneter: {center}")

        p.ChangeDutyCycle(duty)
        sleep(0.25)
        p.ChangeDutyCycle(0)

    # ret is a variable that is returned and determines if a operation was true or not.
    # In our case while it's True then it will run our callback function and display our window.
    ret, image = cam.read()

    # call the detect_face fuction and pass the image parameter
    detect_image = detect_face(image)

    # center of our preview window
    center_screen = (640, 350)

    # circle in the center of the preview window
    cv2.circle(detect_image, (center_screen), 35, (255,0,0), 5)


    
    #img_h = cv2.flip(image, -1)

    cv2.imshow(window_name, detect_image)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        p.stop(0)
        break

cam.release()
cv2.destroyAllWindows()