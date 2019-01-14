#1.	Get user’s skin color before starting the program
#2.	Create box that we will work with, where hand should be placed
#3.	If color is not in threshold of user’s skin, black out that pixel. If it is, set pixel to 1
#4.	This will leave us with just the hand of the user
#5.	Some sort of background removal
#6.	OpenCV find contours

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

#get initial background
_, frame = cap.read()  # don't forget, _ just means we don't care or use return but it is needed
upper_left = (50, 150)
bottom_right = (275, 375)

#set kernel for morphological transformations later on
kernel = np.ones((5,5),np.uint8)

# get the initial frame from the roi
initial_frame = (frame[upper_left[1] + 2: bottom_right[1] - 2, upper_left[0] + 2: bottom_right[0] - 2])
initial_frame = cv2.cvtColor(initial_frame, cv2.COLOR_BGR2GRAY)

while (1):
    _, frame = cap.read() #don't forget, _ just means we don't care or use return but it is needed

    #create roi where gestures will be done
    roi = cv2.rectangle(frame, upper_left, bottom_right, (255, 255, 255), 2)

    # get the frame from the roi, convert it to HSV color space
    current_video = (frame[upper_left[1] + 2: bottom_right[1] - 2, upper_left[0] + 2: bottom_right[0] - 2])
    current_gs = cv2.cvtColor(current_video, cv2.COLOR_BGR2GRAY)

    diffFrame = cv2.absdiff(current_gs, initial_frame)
    diffFrame = cv2.GaussianBlur(diffFrame, (5,5), cv2.BORDER_DEFAULT)
    motion = cv2.threshold(diffFrame, 10, 255, cv2.THRESH_BINARY)[1]

    #fill in black areas inside hand and cancel out noise)
    #motion = cv2.morphologyEx(motion, cv2.MORPH_OPEN, kernel)
    motion = cv2.morphologyEx(motion, cv2.MORPH_DILATE, kernel)
    motion = cv2.morphologyEx(motion, cv2.MORPH_ERODE, kernel)



    #find countours of the image
    filled = np.copy(motion)
    cv2.floodFill(filled, None, (0, 0), 255)
    filled = cv2.bitwise_not(filled)
    motion = cv2.bitwise_or(filled, motion)
    _, contours, hierarchy = cv2.findContours(motion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(current_video, contours, -1, (255, 0, 0), 2)
    cv2.drawContours(motion, contours, -1, (127, 147, 127), 2)



    #flip the frame to make it not a mirror
    cv2.flip(frame, 1);

    cv2.imshow("frame", frame)
    cv2.imshow("current", filled)
    cv2.imshow("diffFrame", diffFrame)
    cv2.imshow("motion", motion)

    k = cv2.waitKey(30) & 0xFF
    if k == 32:
        _, frame = cap.read()
        initial_frame = (frame[upper_left[1] + 2: bottom_right[1] - 2, upper_left[0] + 2: bottom_right[0] - 2])
        initial_frame = cv2.cvtColor(initial_frame, cv2.COLOR_BGR2GRAY)
    if k == 27:
        break


cap.release()
cv2.destroyAllWindows()


