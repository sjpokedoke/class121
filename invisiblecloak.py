import cv2
import numpy as np
import time

#to save the output file
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter("output.avi", fourcc, 20.0, (640, 480))

#starting the camera
cap = cv2.VideoCapture(0)

#allowing the webcam to start by making the code sleep for 2 seconds
time.sleep(2)

bg = 0

#capturing background for 60 frames
for i in range(60):
    ret, bg = cap.read()

#flipping the background
bg = np.flip(bg, axis = 1)

#reading the captured frame until we stop the camera
while(cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    img = np.flip(img, axis = 1)

#converting the colour from bgr to hsv
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#generating mask to detect the colour
lowerred = np.array([0, 120, 50])
upperred = np.array([10, 255, 255])
mask1 = cv2.inRange(hsv, lowerred, upperred)

lowerred = np.array([170, 120, 70])
upperred = np.array([180, 255, 255])
mask2 = cv2.inRange(hsv, lowerred, upperred)

mask1 = mask1+mask2

#adding effects
mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

#selecting only the part that doesn't have mask1
mask2 = cv2.bitwise_not(mask1)

#removing the red colour
reso1 = cv2.bitwise_and(img, img, mask = mask2)
reso2 = cv2.bitwise_and(bg, bg, mask = mask1)

#storing the output
finaloutput = cv2.addWeighted(reso1, 1, reso2, 1, 0)
output_file.write(finaloutput)

#displaying the output to the user
cv2.imshow("magic", finaloutput)
cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()