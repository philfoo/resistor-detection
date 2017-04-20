import cv2
import numpy as np


img = cv2.imread("resistor.jpg")
# ret, thresh = cv2.threshold(img, 127, 255, 0)
# contours, hierarchy = cv2.findContours(thresh, 1, 2)

# cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
# cv2.imshow("test", img)
# cv2.waitKey()

gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite('gray_image.png', gray_image)
cv2.imshow('regular_image', img)

ret, thresh1 = cv2.threshold(gray_image, 235, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresh1, 1, 2)


# Mask stuff
mask = np.zeros(img.shape, np.uint8)
cv2.drawContours(mask, contours, -1, (255), 1)
cv2.imshow("mask", mask)

#Converting to HSV
hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imshow('hsv_image', hsv_image)


#Find most frequent color
#hist = cv2.calcHist([hsv], [0, 1], None, [])

# #Rectangle shit
# for cnt in contours:
# 	approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
# 	if len(approx) == 4:
# 		print "rectangle"
# 		cv2.drawContours(img, [cnt], 0, (255, 0, 0), -1)

#cv2.drawContours(img, contours, -1, (255, 0, 0), 3)
cv2.imshow("test", img)

cv2.waitKey(0)
cv2.destroyAllWindows()
