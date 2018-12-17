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
initial_background = (frame[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]])
initial_background = cv2.cvtColor(initial_background, cv2.COLOR_BGR2HSV)

#this is grabbed from somewhere for testing. Learn it, make it yourself
kernel = np.ones((5,5),np.uint8)

while (1):
    _, frame = cap.read() #don't forget, _ just means we don't care or use return but it is needed

    #create roi where gestures will be done
    roi = cv2.rectangle(frame, upper_left, bottom_right, (255, 255, 255), 2)

    #get the frame from the roi, convert it to HSV color space
    current_video = (frame[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]])
    hsv = cv2.cvtColor(current_video, cv2.COLOR_BGR2HSV)

    #gets the color of the pixel at CENTER of ROI at start of program. This isn't permanant, but works for testing
    hand_center = current_video[112, 112]

    #define lower and upper threshold of skin color (want to make this dynamic somehow, this is an average that shows most skin colors
    lower_limit = np.array(hand_center) - 50
    upper_limit = np.array(hand_center) + 50
    #setting S and V value to encompass all
    lower_limit[1] = 0
    lower_limit[2] = 0
    upper_limit[1] = 255
    upper_limit[2] = 255
    print(lower_limit)
    print(upper_limit)

    #create mask (anywhere a pixel is in the threshold it is white, elsewhere it is black
    mask = cv2.inRange(hsv, lower_limit, upper_limit)
    mask = cv2.dilate(mask, kernel, iterations=1)
    edges = cv2.Canny(mask, 100, 200)

    #apply mask to current video
    current_video = cv2.bitwise_and(current_video, current_video, mask = mask)

    cv2.imshow("frame", frame)
    cv2.imshow("current", current_video)
    cv2.imshow("hand", mask)
    cv2.imshow("edges", edges)

    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()


