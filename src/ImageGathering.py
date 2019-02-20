#1.	This code is the same as the background subtraction, just saves frames when I want it to

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

#setting variables for later
save = 0
count = 0

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

    if save == 1:
        #change directory to match where you are saving, change the break count to say how many frames to capture
        cv2.imwrite("C:/Users/reyfa/Desktop/Design Project Test Codes/tf_files/hand_images/Empty/%s.jpg" % count, motion)
        count += 1
        if count >= 1500:
            break

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
        save = 1
        #if escape is pressed, begin to capture frames



cap.release()
cv2.destroyAllWindows()


