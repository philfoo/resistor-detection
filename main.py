import cv2
import numpy as np
import matplotlib.pyplot as plt
from crop_rectangle import cropRectangle
from skimage.transform import rotate

cap = cv2.VideoCapture(0)
width = int(cap.get(3))
height = int(cap.get(4))

s = np.linspace(0, 2*np.pi, 400)
# x = width/2 + width/3*np.cos(s)
# y = height/2 + height/3*np.sin(s)
x = 300 + 250*np.cos(s)
y = 150 + 150*np.sin(s)
init = np.array([x, y]).T
init = init.astype(int)
pts = init.reshape((-1, 1, 2))
initImg = np.zeros((height, width, 3), dtype='uint8')
cv2.polylines(initImg, [pts], True, (0, 0, 255), thickness=5)

### Reads image from a file
img = cv2.imread("resistor-blue.jpg", cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = rotate(img, 30, mode="edge")
cropRectangle(img, init)


while(True):
    ### Reads image from the computer camera
    # ret, img = cap.read()
    # cv2.imshow("Camera", cv2.add(initImg, img))

    k = cv2.waitKey(1)
    if k & 0xFF == ord('q'):
        break
    elif k & 0xFF == ord('e'):
        ### Convert to rgb since IMREAD_COLOR does bgr
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cropRectangle(img, init)
cap.release()
cv2.destroyAllWindows()
